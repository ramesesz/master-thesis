from manon_chat_interface.utils.llm_utils import (
    ER_SYSTEM_PROMPT, ER_USER_PROMPT, strictjson_llm
)
from strictjson import strict_json


def entity_recognition(
        input: str,
        ):
    """Performs entity recognition on the user input.

    Args:
        input (str): Input of the LLM.
        base_url (_type_, optional): URL where LLM is hosted. Defaults to "http://localhost:1234/v1".
        api_key (str, optional): API key to access LLM. Defaults to "lm-studio".

    Returns:
        _type_: _description_
    """
    response = strict_json(
        system_prompt = ER_SYSTEM_PROMPT,
        user_prompt = ER_USER_PROMPT.format(input=input),
        output_format = {'machine': 'Machine name', 
                         'parts': 'Part name'},
        llm = strictjson_llm
    )

    return response