from manon_chat_interface.utils import llm
from manon_chat_interface.utils import sparql
from strictjson import strict_json

import chromadb


def entity_recognition(input: str) -> dict:
    """
    Performs entity recognition on the provided input string using a large language model (LLM).

    This function identifies and categorizes entities within the user input, specifically separating them into machine and part.

    Multiple 

    Args:
        input (str): The input string to be analyzed by the LLM.

    Returns:
        dict: A dictionary with two keys, 'machines' and 'parts', containing the identified machine names and part names respectively.

    Example:
        Input: "Can Creality Ender manufacture flange?"
        Output: {'machines': ['Creality Ender'], 'parts': ['flange']}

    """
    response = strict_json(
        system_prompt=llm.ER_SYSTEM_PROMPT,
        user_prompt=llm.ER_USER_PROMPT.format(input=input),
        output_format={"pizza": "Array of pizza", 
                       "topping": "Array of topping"},
        llm=llm.invoke_llm
    )

    return response


def get_triples(client, question, entity, collection_name, mode, url):
    """Helper function for retrieve_context()

    Args:
        client (chromadb.PersistentClient): Chroma client.
        entity (list(str)): Entity being queried to chroma.
        collection_name (_type_): Chromadb collection.
        mode (_type_): Mode of context retrieval.
        url (_type_): LM Studio URL.

    Returns:
        str: SPARQL query.
    """
    if entity:
        collection = client.get_or_create_collection(collection_name)
        embeddings = collection.query(query_texts=entity, n_results=1)
        iris = [metadata['IRI'] for metadata in embeddings['metadatas'][0]]
        if mode == "default":
            # Use generic sparql queries to retrieve tables for context
            # queries = [sparql.GET_CLASSES, sparql.GET_CLASS_HIERARCHY, sparql.GET_PROPERTIES]
            queries = [sparql.ALL_TRIPLES_QUERY]
            context = sparql.execute_parse_sparql(url, queries) # Result prefixes already replaced
            return context
        elif mode == "n_hop":
            # Additional handling for n_hop mode
            pass
        else:
            # Handle other modes if necessary
            pass


def retrieve_context(entities: dict, # From entity recognition
                     question: str, # From question
                     path: str, # Path to vectorstore
                     mode: str = "default", 
                     url: str = "http://localhost:3030/pizza/query"
                     ):
    try:
        client = chromadb.PersistentClient(path=path)
        pizza_info = get_triples(client, question, entities.get("pizza"), "pizza_collection", mode, url)
        topping_info = get_triples(client, question, entities.get("topping"), "topping_collection", mode, url)
        return {
            "pizza": pizza_info,
            "topping": topping_info
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
