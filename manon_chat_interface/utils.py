import chromadb
import uuid

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
    # Create a list of unique ids for each document based on the content
    ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, document)) for document in documents]
    unique_ids = list(set(ids))

    # Ensure that only docs that correspond to unique ids are kept and that only one of the duplicate ids is kept
    seen_ids = set()
    unique_docs = [document for document, id in zip(documents, ids) if id not in seen_ids and (seen_ids.add(id) or True)]

    # Remove duplicates by comparing generated unique_ids and embedded ids
    client = chromadb.PersistentClient(path=path)
    collection = client.get_or_create_collection(name=collection)
    existing_ids = collection.get()["ids"]

    # Filter out the unique_ids and unique_docs if the unique_id is already in existing_ids
    filtered_pairs = [(uid, doc) for uid, doc in zip(unique_ids, unique_docs) if uid not in existing_ids]

    # Embed if unique docs is not empty
    if filtered_pairs:
        unique_ids, unique_docs = zip(*filtered_pairs)

        collection.add(
            documents=list(unique_docs),
            ids=list(unique_ids),
            metadatas=[{"IRI": iri} for iri in iris]
        )