EXTRACTION_QUERY_TEMPLATE = """
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX ManO: <http://www.ontology.ift.dlr.de/MANON/ManOnSTEP#>
  PREFIX om-2: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
  PREFIX Feat: <http://www.ontology.ift.dlr.de/MANON/Features#>
  PREFIX ManO2: <http://www.ontology.ift.dlr.de/MANON/ManOn#>
  PREFIX Part: <http://www.ontology.ift.dlr.de/MANON/Parts#>
  PREFIX Rest: <http://www.ontology.ift.dlr.de/MANON/Restrictions#>
  PREFIX Tole: <http://www.ontology.ift.dlr.de/MANON/Tolerances#>
  SELECT ?individual
  WHERE {{
    ?class rdfs:subClassOf* <{iri}> .
    ?individual rdf:type ?class .
  }}
"""


ONE_HOP_EXTRACTION_QUERY = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX ManO: <http://www.ontology.ift.dlr.de/MANON/ManOnSTEP#>
PREFIX om-2: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
PREFIX Feat: <http://www.ontology.ift.dlr.de/MANON/Features#>
PREFIX ManO2: <http://www.ontology.ift.dlr.de/MANON/ManOn#>
PREFIX Part: <http://www.ontology.ift.dlr.de/MANON/Parts#>
PREFIX Rest: <http://www.ontology.ift.dlr.de/MANON/Restrictions#>
PREFIX Tole: <http://www.ontology.ift.dlr.de/MANON/Tolerances#>
SELECT ?subject ?predicate ?object
WHERE {
  {
    <http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> ?predicate ?object .
    BIND(<http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> AS ?subject)
  }
  UNION
  {
    ?subject <http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> ?object .
    BIND(<http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> AS ?predicate)
  }
  UNION
  {
    ?subject ?predicate <http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> .
    BIND(<http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> AS ?object)
  }
}
"""


TWO_HOP_EXTRACTION_QUERY = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX ManO: <http://www.ontology.ift.dlr.de/MANON/ManOnSTEP#>
PREFIX om-2: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
PREFIX Feat: <http://www.ontology.ift.dlr.de/MANON/Features#>
PREFIX ManO2: <http://www.ontology.ift.dlr.de/MANON/ManOn#>
PREFIX Part: <http://www.ontology.ift.dlr.de/MANON/Parts#>
PREFIX Rest: <http://www.ontology.ift.dlr.de/MANON/Restrictions#>
PREFIX Tole: <http://www.ontology.ift.dlr.de/MANON/Tolerances#>

SELECT ?subject ?predicate ?object
WHERE {
  {
    <http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> ?predicate ?object .
    BIND(<http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> AS ?subject)
  }
  UNION
  {
    ?subject <http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> ?object .
    BIND(<http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> AS ?predicate)
  }
  UNION
  {
    ?subject ?predicate <http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> .
    BIND(<http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> AS ?object)
  }
  UNION
  {
    <http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> ?p1 ?intermediateNode .
    ?intermediateNode ?p2 ?object2 .
    BIND(<http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> AS ?subject)
    BIND(?p1 AS ?predicate)
    BIND(?object2 AS ?object)
  }
  UNION
  {
    ?subject2 ?p1 <http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> .
    ?subject2 ?p2 ?object .
    BIND(<http://www.ontology.ift.dlr.de/MANON/EOSM290#M_EOSM290> AS ?objectBound)
    BIND(?p1 AS ?predicate)
    BIND(?subject2 AS ?subject)
  }
}
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
