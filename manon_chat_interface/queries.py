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