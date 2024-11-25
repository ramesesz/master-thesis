from manon_chat_interface.utils import utils
from urllib.error import URLError
from rdflib import Graph, BNode
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
    try:
      wrapper = SPARQLWrapper(url)
      wrapper.setQuery(query)
      wrapper.setReturnFormat(JSON)
      results = wrapper.query().convert()

    except URLError as e:
        print(f"\033[91mERROR. SPARQL server may not be running.\033[0m Error message: {e}")
        
    return results


def load_rdf_triples(file_path: str, format: str = 'ttl'):
  # gaada prefix jadi ngarang dia
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


prefix_dict = {
    "atm:": "https://data.nasa.gov/ontologies/atmonto/ATM#",
    "eqp:": "https://data.nasa.gov/ontologies/atmonto/equipment#",
    "gen:": "https://data.nasa.gov/ontologies/atmonto/general#",
    "nas:": "https://data.nasa.gov/ontologies/atmonto/NAS#",
    "owl:": "http://www.w3.org/2002/07/owl#",
    "rdf:": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs:": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd:": "http://www.w3.org/2001/XMLSchema#"
}

PREFIXES = """
PREFIX atm: <https://data.nasa.gov/ontologies/atmonto/ATM#>
PREFIX eqp: <https://data.nasa.gov/ontologies/atmonto/equipment#>
PREFIX gen: <https://data.nasa.gov/ontologies/atmonto/general#>
PREFIX nas: <https://data.nasa.gov/ontologies/atmonto/NAS#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

########################################################################
## Embed entities ######################################################
########################################################################
EXTRACTION_QUERY = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT DISTINCT ?classIRI ?classLabel ?classComment ?entity ?entityLabel ?entityComment
WHERE {
    {
        ?classIRI a owl:Class .
        OPTIONAL { ?classIRI rdfs:label ?classLabel . }
        OPTIONAL { ?classIRI rdfs:comment ?classComment . }
    }
    UNION
    {
        ?entity a ?classIRI .
        ?classIRI a owl:Class .
        OPTIONAL { ?entity rdfs:label ?entityLabel . }
        OPTIONAL { ?entity rdfs:comment ?entityComment . }
    }
}
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
