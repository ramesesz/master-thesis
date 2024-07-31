from openai import OpenAI

########################################################################
## Entity recognition ##################################################
########################################################################
ER_SYSTEM_PROMPT = """
You are an expert in the gastronomy domain with extensive knowledge of various pizzas and toppings. Your task is to 
accurately identify and extract the names of pizzas and toppings from given text. You should focus on recognizing 
specific terminology and contextually relevant phrases that pertain to pizza names and their toppings 
within the gastronomy sector. Your output should be in JSON format, categorizing the identified terms into "pizza" 
and "topping". The output should be strictly the JSON object without any additional commentary or explanation.
"""

ER_USER_PROMPT = """
I want you to identify the pizza and topping of the following input.

Input: {input}
Output: 
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

# TODO: Enhance the prompt. Currently it does not answer the question and instead just explains the context
QA_USER_PROMPT = """
Question: {question}
"""


def generate_response(user_prompt: str, messages: list):
    """Calls the LLM with history.
        input (str): Input of the LLM.
        messages (list): History of messages.
    """
    try:
        user_message = {"role": "user", "content": user_prompt}
        messages.append(user_message)

        client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

        response = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
            messages=messages,
            temperature=1,
        )

        new_message = {"role": "assistant", "content": response.choices[0].message.content}
        messages.append(new_message)
    
    except Exception as e:
        print(f"An error occured when invoking the LLM: {e}")

    return response, messages


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
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]   

        client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

        response = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
            messages=messages,
            temperature=1,
        )

    except Exception as e:
        print(f"An error occured when invoking the LLM: {e}")
    
    return response.choices[0].message.content