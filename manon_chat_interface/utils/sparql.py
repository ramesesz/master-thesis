prefix_dict = {
    ":": "http://www.co-ode.org/ontologies/pizza#",
    "dc:": "http://purl.org/dc/elements/1.1/",
    "owl:": "http://www.w3.org/2002/07/owl#",
    "rdf:": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "xml:": "http://www.w3.org/XML/1998/namespace",
    "xsd:": "http://www.w3.org/2001/XMLSchema#",
    "rdfs:": "http://www.w3.org/2000/01/rdf-schema#",
    "skos:": "http://www.w3.org/2004/02/skos/core#",
    "pizza:": "http://www.co-ode.org/ontologies/pizza/pizza.owl#",
    "terms:": "http://purl.org/dc/terms/",
    "base:": "http://www.co-ode.org/ontologies/pizza#"
}

PREFIXES = """
PREFIX : <http://www.co-ode.org/ontologies/pizza#> 
PREFIX dc: <http://purl.org/dc/elements/1.1/> 
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX xml: <http://www.w3.org/XML/1998/namespace> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
PREFIX pizza: <http://www.co-ode.org/ontologies/pizza/pizza.owl#> 
PREFIX terms: <http://purl.org/dc/terms/> 
BASE <http://www.co-ode.org/ontologies/pizza#> 
"""

########################################################################
## Embed entities ######################################################
########################################################################
EXTRACTION_QUERY = """
SELECT DISTINCT ?individual
WHERE {{
{{
 SELECT ?individual
 WHERE {{
   ?individual rdfs:subClassOf* {pizza_class} .
 }}
}}
UNION
{{
 SELECT DISTINCT ?individual
 WHERE {{
   ?individual rdf:type owl:Class ;
           owl:equivalentClass ?equivClass .

   ?equivClass owl:intersectionOf ?list .
   ?list rdf:rest*/rdf:first {pizza_class} .
 }}
}}
}}
"""

########################################################################
## Golden standard #####################################################
########################################################################
PIZZA_RESTRICTIONS = """
SELECT DISTINCT ?pizza ?property ?type ?value
WHERE {{
  BIND({pizza_variable} AS ?pizza)  
  ?pizza rdfs:subClassOf ?restriction .
  ?restriction rdf:type owl:Restriction ;
               owl:onProperty ?property .

  OPTIONAL {{
    ?restriction owl:someValuesFrom ?value .
    BIND(owl:someValuesFrom AS ?type)
  }}
  OPTIONAL {{
    ?restriction owl:hasValue ?value .
    BIND(owl:hasValue AS ?type)
  }}
}}
"""

PIZZA_TRIPLES = """
SELECT DISTINCT ?subject ?predicate ?object
WHERE {{
  {{
    BIND({pizza_variable} AS ?subject) .
    ?subject ?predicate ?object .
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
  UNION
  {{
    BIND({pizza_variable} AS ?object) .
    ?subject ?predicate ?object .
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
}}
"""

########################################################################
## T-Box ###############################################################
########################################################################
GET_CLASSES = """
SELECT ?class ?label
WHERE {
  {
    ?class rdf:type owl:Class .
    FILTER (isIRI(?class))
    OPTIONAL { ?class rdfs:label ?label . }
  }
  UNION
  {
    ?class rdf:type rdfs:Class .
    FILTER (isIRI(?class))
    OPTIONAL { ?class rdfs:label ?label . }
  }
}
"""

GET_PROPERTIES = """
SELECT ?property ?domain ?range ?label
WHERE {
  {
    ?property rdf:type owl:ObjectProperty .
    FILTER (isIRI(?property))
    OPTIONAL { ?property rdfs:domain ?domain . }
    OPTIONAL { ?property rdfs:range ?range . }
    OPTIONAL { ?property rdfs:label ?label . }
  }
  UNION
  {
    ?property rdf:type owl:DatatypeProperty .
    FILTER (isIRI(?property))
    OPTIONAL { ?property rdfs:domain ?domain . }
    OPTIONAL { ?property rdfs:range ?range . }
    OPTIONAL { ?property rdfs:label ?label . }
  }
}
"""

GET_CLASS_HIERARCHY = """
SELECT ?subClass ?superClass
WHERE {
  ?subClass rdfs:subClassOf ?superClass .
  FILTER (isIRI(?subClass) && isIRI(?superClass))
}
"""

########################################################################
## n-Hop ###############################################################
########################################################################


from SPARQLWrapper import SPARQLWrapper, JSON

import pandas as pd

def execute_sparql(url: str, query: str):
    """    
    Executes a SPARQL query against a specified endpoint.

    This function sends a SPARQL query to the given endpoint URL and returns the results in JSON format.

    Args:
        url (str): The URL of the SPARQL query endpoint.
        query (str): The SPARQL query to be executed.

    Returns:
        dict: The results of the SPARQL query in JSON format.
    """
    wrapper = SPARQLWrapper(url)
    wrapper.setQuery(query)
    wrapper.setReturnFormat(JSON)
    results = wrapper.query().convert()

    return results


def execute_parse_sparql(url, queries):
    """Helper function for retrieve_context().

    Args:
        url (_type_): _description_
        queries (_type_): _description_

    Returns:
        _type_: _description_
    """
    results = []
    for index, query in enumerate(queries):
        result = execute_sparql(url=url, query=query)
        table = parse_sparql_output(result).to_string()
        results.append(f"Triples: {index}\n{table}")
    subgraph = "\n".join(results)
    subgraph = replace_urls_with_prefixes(subgraph, prefix_dict)
    return subgraph


def parse_sparql_output(query_output: dict):
    """Parse query JSON output to dataframe.

    Args:
        query_output (dict): The output from a SPARQL query in JSON format

    Returns:
        pd.DataFrame: the parsed results as a pandas DataFrame
    """
    columns = query_output['head']['vars']
    rows = []
    for result in query_output['results']['bindings']:
        row = {}
        for col in columns:
            row[col] = result[col]['value'] if col in result else None
        rows.append(row)
    df = pd.DataFrame(rows, columns=columns)
    return df


def replace_urls_with_prefixes(text, prefix_dict):
    """Replace URLs with prefixes in a given string.

    Args:
        text (str): String containing SPARQL query or text.
        prefix_dict (dict): Mapping of prefixes to URLs.
    """
    for prefix, url in prefix_dict.items():
        text = text.replace(url, prefix)
    return text


def replace_prefixes_with_urls(text, prefix_dict):
    """Replace prefixes with URLs in a given string.

    Args:
        text (str): String containing SPARQL query or text.
        prefix_dict (dict): Mapping of prefixes to URLs.
    """
    for prefix, url in prefix_dict.items():
        text = text.replace(prefix, url)
    return text


def generate_sparql_n_hop_query(starting_node, prefixes, n_hops):
    """
    Generate a SPARQL query that retrieves all triples within n-hops from a starting node.

    Parameters:
    - starting_node (str): The URI of the starting node.
    - n_hops (int): The maximum number of hops to traverse.

    Returns:
    - str: A SPARQL query string.
    """
    # The base predicate pattern to match any predicate (adjust as needed)
    predicate_pattern = "?p"

    # Construct the SPARQL query with variable path length up to n_hops
    query = f"""
    {prefixes}
    SELECT ?subject ?predicate ?object
    WHERE {{
        {starting_node} ?predicate* ?object .
        ?subject ?predicate* ?object .
        ?subject ?predicate ?object .
        FILTER(isIRI(?object))  # Optional: Ensure that objects are IRI nodes, not literals
    }}
    """
    return query