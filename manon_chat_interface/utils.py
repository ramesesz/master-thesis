import chromadb

from SPARQLWrapper import SPARQLWrapper, JSON

def execute_sparql(url: str, query: str):
    """Execute a SPARQL Query

    Args:
        url (str): URL of the SPARQL query endpoint.
        query (str): SPARQL query to be executed.

    Returns:
        json: Results of the SPARQL query.
    """
    wrapper = SPARQLWrapper(url)
    wrapper.setQuery(query)
    wrapper.setReturnFormat(JSON)
    results = wrapper.query().convert()

    return results


def embed_entities(path: str, collection: str, documents: list, iris: list):
    """Embed entities to vectorstore

    Args:
        path (str): Path to vectorstore.
        collection (str): Name of collection.
        documents (list): List of documents.
        iris (list): List of iris of the documents.
    """
    client = chromadb.PersistentClient(path=path)
    collection = client.get_or_create_collection(name=collection)
    collection.add(
        documents=documents,
        ids=documents,
        metadatas=[{"IRI": iri} for iri in iris]
    )