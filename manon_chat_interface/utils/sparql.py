from manon_chat_interface.utils import utils
from urllib.error import URLError
from rdflib import Graph, BNode
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
    try:
      wrapper = SPARQLWrapper(url)
      wrapper.setQuery(query)
      wrapper.setReturnFormat(JSON)
      results = wrapper.query().convert()

    except URLError as e:
        print(f"\033[91mERROR. Server may not be running.\033[0m Error message: {e}")
        
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
        result = execute_sparql(url=url, query=PREFIXES+query)
        table = utils.parse_sparql_output(result).to_string()
        results.append(f"Triples: {index}\n{table}")
    subgraph = "\n".join(results)
    subgraph = utils.replace_urls_with_prefixes(subgraph, prefix_dict)
    return subgraph


def load_rdf_triples(file_path: str, format: str = 'ttl'):
    
  # Create a Graph object 
  g = Graph()
  g.parse(file_path, format=format)

  # Retrieve triples whose subject and object are not blank nodes
  triples_string = ""
  for subj, pred, obj in g:
      if not isinstance(subj, BNode) and not isinstance(obj, BNode):
          triples_string += f"{subj} {pred} {obj} .\n"

  replaced_triples_string = utils.replace_urls_with_prefixes(triples_string, prefix_dict)

  return replaced_triples_string


# TODO: Fix this function
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
## n-Hop ###############################################################
########################################################################
ONE_HOP = """
SELECT ?subject ?predicate ?object WHERE {{
  {{
    ?s ?p <{IRI}> .
    BIND(?s AS ?subject)
    BIND(?p AS ?predicate)
    BIND(<{IRI}> AS ?object)
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
  UNION
  {{
    <{IRI}> ?p ?o .
    BIND(<{IRI}> AS ?subject)
    BIND(?p AS ?predicate)
    BIND(?o AS ?object)
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
}}
"""

TWO_HOP = """
SELECT ?subject ?predicate ?object WHERE {{
  {{
    ?s ?p <{IRI}> .
    BIND(?s AS ?subject)
    BIND(?p AS ?predicate)
    BIND(<{IRI}> AS ?object)
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
  UNION
  {{
    ?s ?p <{IRI}> .
    ?s1 ?p1 ?s .
    BIND(?s1 AS ?subject)
    BIND(?p1 AS ?predicate)
    BIND(?s AS ?object)
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
  UNION
  {{
    <{IRI}> ?p ?o .
    BIND(<{IRI}> AS ?subject)
    BIND(?p AS ?predicate)
    BIND(?o AS ?object)
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
  UNION
  {{
    <{IRI}> ?p ?o .
    ?o ?p1 ?o1 .
    BIND(?o AS ?subject)
    BIND(?p1 AS ?predicate)
    BIND(?o1 AS ?object)
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
}}
"""

THREE_HOP = """
SELECT ?subject ?predicate ?object WHERE {{
  {{
    ?s ?p <{IRI}> .
    BIND(?s AS ?subject)
    BIND(?p AS ?predicate)
    BIND(<{IRI}> AS ?object)
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
  UNION
  {{
    ?s ?p <{IRI}> .
    ?s1 ?p1 ?s .
    BIND(?s1 AS ?subject)
    BIND(?p1 AS ?predicate)
    BIND(?s AS ?object)
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
  UNION
  {{
    ?s ?p <{IRI}> .
    ?s1 ?p1 ?s .
    ?s2 ?p2 ?s1 .
    BIND(?s2 AS ?subject)
    BIND(?p2 AS ?predicate)
    BIND(?s1 AS ?object)
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
  UNION
  {{
    <{IRI}> ?p ?o .
    BIND(<{IRI}> AS ?subject)
    BIND(?p AS ?predicate)
    BIND(?o AS ?object)
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
  UNION
  {{
    <{IRI}> ?p ?o .
    ?o ?p1 ?o1 .
    BIND(?o AS ?subject)
    BIND(?p1 AS ?predicate)
    BIND(?o1 AS ?object)
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
  UNION
  {{
    <{IRI}> ?p ?o .
    ?o ?p1 ?o1 .
    ?o1 ?p2 ?o2 .
    BIND(?o1 AS ?subject)
    BIND(?p2 AS ?predicate)
    BIND(?o2 AS ?object)
    FILTER (!isBlank(?subject) && !isBlank(?object))
  }}
}}
"""
