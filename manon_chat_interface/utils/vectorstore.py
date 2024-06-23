import chromadb
import uuid


def embed_entities(path: str, collection: str, documents: list, metadatas: list = None):
    """    
    Embed entities into a vectorstore.

    This function embeds a list of documents into a specified vectorstore collection, ensuring uniqueness based on document content.
    
    Args:
        path (str): The file system path to the vectorstore.
        collection (str): The name of the collection within the vectorstore.
        documents (list): A list of documents to be embedded.
        metadatas (list, optional): A list of metadata dictionaries corresponding to the documents.
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
            metadatas=metadatas
        )
