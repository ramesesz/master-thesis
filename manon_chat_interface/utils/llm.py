from openai import OpenAI
from strictjson import strict_json

import chromadb

def generate_sparql_query(path_to_graph, question, mode):
    # Load turtle file for system prompt context
    with open(path_to_graph, 'r', encoding='utf-8') as file:
        ttl_content = file.read()

    # Get entity metadata
    path_to_vectorstore = "../data/vectorstores/flight_vectorstore"
    client = chromadb.PersistentClient(path=f"{path_to_vectorstore}")
    collection = client.get_or_create_collection("flight_collection")

    entities = entity_recognition(question)["entities"]

    embeddings = collection.query(
        query_texts=entities, n_results=1
    )

    query = strict_json(
        system_prompt=TEXT2SPARQL_SYSTEM_PROMPT.format(
            context=ttl_content
        ),
        user_prompt=TEXT2SPARQL_USER_PROMPT.format(
            question=question, metadata=str(embeddings)
        ),
        output_format={
            "sparql_query": "Executable sparql query string.", 
            "explanation": "Explanation of what the sparql query does."
        },
        llm=invoke_huggingface if mode == "huggingface" else invoke_llm
    )

    return query


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

    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    print("Generating with local model...")

    response = client.chat.completions.create(
        model="TheBloke/Meta-Llama-3.1-8B-Instruct-GGUF",
        messages=messages,
        temperature=0,
    )

    return response.choices[0].message.content


def invoke_huggingface(system_prompt: str, user_prompt: str):
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

    # Insert your API key here. Environ settings not set up, key needs to be hard-coded.
    client = OpenAI(base_url="https://api-inference.huggingface.co/v1/", api_key="XXX")

    print("Generating with huggingface model...")

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.1-70B-Instruct",
        messages=messages,
        temperature=0,
        max_tokens=800
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
TEXT2SPARQL_SYSTEM_PROMPT = """
You are a helpful assistant with expertise in SPARQL. Write a SPARQL query that retrieves triples relevant for the question given by the user following the restrictions:
-The goal of the query is to retrieve relevant triples, not directly answering the question;
-Do not limit the query results;
-Use only prefixes, classes and properties provided in the RDF graph;
-Use the IRIs provided in the object metadata given along the question to construct the query;
-Declare non-essential properties to the question as OPTIONAL if needed

Consider the following RDF graph in Turtle syntax:
    {context}

Your output should be in JSON format, categorizing the identified terms into "sparql_query" and "explanation". The output should be strictly the JSON object without any additional commentary or explanation.
"""

TEXT2SPARQL_USER_PROMPT = """
Question: {question}
Object metadata: {metadata}
"""

########################################################################
## QA prompt template ##################################################
########################################################################
TRIPLE2TEXT_SYSTEM_PROMPT = """
You are an expert assistant specialized in RDF graphs. Answer the user’s question using only the information from the RDF triples, providing a full, concise answer in one or two sentences.
Triples: {triples}
"""

# TODO: Enhance the prompt.
TRIPLE2TEXT_USER_PROMPT = """
Question: {question}
"""
