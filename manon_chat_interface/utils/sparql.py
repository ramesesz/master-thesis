MACHINE_EXTRACTION_QUERY = """
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
  WHERE {
    ?class rdfs:subClassOf* <http://www.ontology.ift.dlr.de/MANON/Machines#ManufacturingMachine> .
    ?individual rdf:type ?class .
  }
"""

PART_EXTRACTION_QUERY = """
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
  WHERE {
    ?class rdfs:subClassOf* <http://www.ontology.ift.dlr.de/MANON/Parts#Part> .
    ?individual rdf:type ?class .
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
