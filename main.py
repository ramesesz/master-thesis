from manon_chat_interface.utils import orchestration, sparql, utils, llm

import chromadb

# Define question
question = "Can I make an american pizza with mozzarella topping?"

# TODO: Apply cosine threshold and entity not found handling.

# Get triples
triples = orchestration.get_triples(
    question=question, 
    mode="generated",
    path_to_vectorstore="./manon_chat_interface/data/vectorstores",
    path_to_graph="./manon_chat_interface/data/ontologies/pizza.ttl",
    format="ttl"
)
# try:
#     response = llm.invoke_llm(
#         system_prompt=llm.QA_SYSTEM_PROMPT.format(context=triples),
#         user_prompt=llm.QA_USER_PROMPT.format(question=original_question)
#     )
#     print(response)
# except Exception as e:
#     print(f"The following error occured {e}")

print(triples)
