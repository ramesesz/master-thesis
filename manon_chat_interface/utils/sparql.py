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

# Formatable
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

# Formatable
PIZZA_RESTRICTIONS = """
SELECT ?restriction ?property ?type ?value
WHERE {{
  {pizza_name} rdfs:subClassOf ?restriction .
  ?restriction rdf:type owl:Restriction ;
               owl:onProperty ?property .

  OPTIONAL {{
    ?restriction owl:someValuesFrom ?value .
    BIND("someValuesFrom" AS ?type)
  }}
  OPTIONAL {{
    ?restriction owl:allValuesFrom ?value .
    BIND("allValuesFrom" AS ?type)
  }}
  OPTIONAL {{
    ?restriction owl:hasValue ?value .
    BIND("hasValue" AS ?type)
  }}
}}
"""



from SPARQLWrapper import SPARQLWrapper, JSON

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
