from SPARQLWrapper import SPARQLWrapper, JSON

def execute_sparql(wrapper, query):
    """Execute a SPARQL Query

    Args:
        wrapper (SPARQLWrapper.SPARQLWrapper): A wrapper for a SPARQL query endpoint.
        query (str): SPARQL query to be executed.

    Returns:
        json: Results of the SPARQL query.
    """
    wrapper.setQuery(query)

    wrapper.setReturnFormat(JSON)

    results = wrapper.query().convert()

    return results