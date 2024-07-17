from openai import OpenAI

ER_SYSTEM_PROMPT = """
You are an expert in the gastronomy domain with extensive knowledge of various pizzas and toppings. Your task is to accurately identify and extract the names of machines and parts from given text. You should 
focus on recognizing specific terminology and contextually relevant phrases that pertain to pizza names and their toppings 
within the gastronomy sector. Your output should be in JSON format, categorizing the identified terms into "pizza" 
and "topping". The output should be strictly the JSON object without any additional commentary or explanation.
"""

ER_USER_PROMPT = """
I want you to identify the pizza and topping of the following input.

Input: {input}
Output: 
"""

CONTEXT_RETRIEVAL_SYSTEM_PROMPT = """
You are an expert SPARQL-based context retrieval. You will be given a question and the relevant entities
within it. Your task is to help generate a SPARQL query that represents given question. Make sure to give
only the executable SPARQL query in your answer.
"""

CONTEXT_RETRIEVAL_USER_PROMPT = """
Here are the IRIs of the entity in question: {iris}
Consider the following subgraph in turtle syntax: {subgraph}
Given the question: {question}
Create a SPARQL query that best represent the question.
SPARQL query:
"""

def generate_response(client: OpenAI, input: str, messages: list):
    """Sends a request to local LMStudio server and generate LLM response. Appends prompt 
    and response to messages.
        input (str): Input of the LLM.
        messages (list): History of messages.
    """

    input_message = {"role": "user", "content": input}
    messages.append(input_message)

    response = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=messages,
        temperature=0.7,
    )

    new_message = {"role": "assistant", "content": response.choices[0].message.content}
    messages.append(new_message)

    return response, messages


def invoke_llm(system_prompt: str, user_prompt: str):
    """LLM function call to be passed to strictjson.strict_json().
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

    response = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=messages,
        temperature=0.7,
    )
    
    return response.choices[0].message.content