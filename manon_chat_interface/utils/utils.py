from manon_chat_interface.utils.llm import (
    ER_SYSTEM_PROMPT, ER_USER_PROMPT, strictjson_llm
)
from strictjson import strict_json


def entity_recognition(input: str) -> dict:
    """
    Performs entity recognition on the provided input string using a large language model (LLM).

    This function identifies and categorizes entities within the user input, specifically separating them into machines and parts.

    Args:
        input (str): The input string to be analyzed by the LLM.

    Returns:
        dict: A dictionary with two keys, 'machines' and 'parts', containing the identified machine names and part names respectively.

    Example:
        Input: "Can Creality Ender manufacture flange?"
        Output: {'machines': 'Creality Ender', 'parts': 'flange'}

    """
    response = strict_json(
        system_prompt=ER_SYSTEM_PROMPT,
        user_prompt=ER_USER_PROMPT.format(input=input),
        output_format={'machines': 'Machine name', 
                       'parts': 'Part name'},
        llm=strictjson_llm
    )

    return response



def retrieve_context():
    
    
    pass 
