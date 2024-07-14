from manon_chat_interface.utils.llm import (
    ER_SYSTEM_PROMPT, ER_USER_PROMPT, strictjson_llm
)
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
        system_prompt=ER_SYSTEM_PROMPT,
        user_prompt=ER_USER_PROMPT.format(input=input),
        output_format={"pizza": "Array of pizza", 
                       "topping": "Array of topping"},
        llm=strictjson_llm
    )

    return response


def retrieve_context(entities, path):
    client = chromadb.PersistentClient(path=path)
    if entities["pizza"]:
        collection = client.get_or_create_collection("pizza_collection")
        embeddings = collection.query(
            query_texts=entities["machines"],
            n_results=1
        )
        # TODO: Exec query using IRI
    if entities["topping"]:
        collection = client.get_or_create_collection("topping_collection")
        # TODO: Exec query using IRI
    
    pass 
