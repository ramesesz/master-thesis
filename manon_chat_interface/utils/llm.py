from openai import OpenAI
from dotenv import load_dotenv
from strictjson import strict_json

import os

load_dotenv()
LLM_ENDPOINT = os.getenv('LLM_ENDPOINT')


def entity_recognition(input: str) -> dict:
    """
    Performs entity recognition on the provided input string using a large language model (LLM).

    This function identifies and categorizes entities within the user input.

    Multiple 

    Args:
        input (str): The input string to be analyzed by the LLM.

    Returns:
        dict: A dictionary with key 'entities', containing the identified entities within the question.

    Example:
        Input: "Can Creality Ender manufacture flange?"
        Output: {'entities': ['Creality Ender', 'flange']}

    """
    response = strict_json(
        system_prompt=ER_SYSTEM_PROMPT,
        user_prompt=ER_USER_PROMPT.format(input=input),
        output_format={"entities": "Array of entities"},
        llm=invoke_llm
    )

    return response


def invoke_llm(system_prompt: str, user_prompt: str):
    """Calls the LLM without history.
    LLM function call to be passed to strictjson.strict_json(). It is advised not to change the parameters.
    Refer to https://github.com/tanchongmin/strictjson/blob/main/strictjson/base.py#L319

    Args:
        system_prompt (str): System prompt.
        user_prompt (str): User prompt.

    Returns:
        str: LLM response string.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]   

    client = OpenAI(base_url=LLM_ENDPOINT, api_key="lm-studio")

    response = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
        messages=messages,
        temperature=1,
    )

    return response.choices[0].message.content


########################################################################
## Entity recognition ##################################################
########################################################################
ER_SYSTEM_PROMPT = """
You are an expert in the aviation domain with extensive knowledge of various flight-related 
concepts. Your task is to accurately identify and extract the names of entities from the given 
text. Focus on recognizing specific terminology and contextually relevant phrases that pertain 
to objects such as flights, airlines, airports, aircraft types, and aviation operations. Your 
output should be in JSON format, placing the identified terms into the key 'entities'. For 
instance, {'entities': ['Flight123', 'Airbus A320', 'JFK Airport']}. The output should be 
strictly the JSON object without any additional commentary or explanation.
"""

ER_USER_PROMPT = """
I want you to identify the entities of the following input.

Input: {input}
"""

########################################################################
## SPARQL generation ###################################################
########################################################################
CONTEXT_RETRIEVAL_SYSTEM_PROMPT = """
You are a helpful assistant. I want you to answer generate a SPARQL query considering the question given by the user and the following pandas DataFrame containing RDF triples:
    {context}
-Use only classes and properties defined in the RDF graph, for this is important to use the same URIs for the properties and classes as defined in the original graph; 
-Include all the prefixes used in the SPARQL query; 
-Declare non-essential properties to the question as OPTIONAL if needed; 
-DO NOT use specific resources in the query; Declare filters on strings (like labels and names) as filter operations over the REGEX function using the case-insensitive flag.

Your output should be in JSON format, categorizing the identified terms into "sparql_query" and "explanation". The output should be strictly the JSON object without any additional commentary or explanation.
"""

CONTEXT_RETRIEVAL_USER_PROMPT = """
Question: {question}
"""

########################################################################
## QA prompt template ##################################################
########################################################################
QA_SYSTEM_PROMPT = """
You are a helpful assistant. I want you to answer the given user question considering the context given in the
following RDF triples. Explain your reasoning and cite the relevant triples
Triples: {context}
"""

# TODO: Enhance the prompt.
QA_USER_PROMPT = """
Question: {question}
"""
