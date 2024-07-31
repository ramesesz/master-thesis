from manon_chat_interface.utils import orchestration, sparql, utils, llm

import chromadb

# Get chroma
path_to_entities = "./manon_chat_interface/data/vectorstores/pizza_entities"
path_to_questions = "./manon_chat_interface/data/vectorstores/pizza_questions"

entities_client = chromadb.PersistentClient(path=path_to_entities)
questions_client = chromadb.PersistentClient(path=path_to_questions)


# Get question
original_question = "Can I make an american pizza with mozzarella topping?"
question_collection = questions_client.get_or_create_collection("pizza_questions")
question_emb = question_collection.query(
    query_texts=[original_question], n_results=1
)
mapped_question = question_emb["documents"][0][0] # Context

# Get entities' IRIs
pizza_collection = entities_client.get_or_create_collection("pizza_collection")
topping_collection = entities_client.get_or_create_collection("topping_collection")

entity = orchestration.entity_recognition(original_question)
recognized_pizza = entity["pizza"]
recognized_topping = entity["topping"]

mapped_pizza = pizza_collection.query(
    query_texts=recognized_pizza,
    n_results=1
)
pizza_iri = mapped_pizza["metadatas"][0][0]["IRI"] # Context

mapped_topping = topping_collection.query(
    query_texts=recognized_topping,
    n_results=1
)
topping_iri = mapped_pizza["metadatas"][0][0]["IRI"] # Used for LLM SPARQL generation. Not in use right now.

# Get triples
triples = orchestration.get_triples(
    entities_client, 
    original_question, 
    recognized_pizza,
    "pizza_collection",
    mode="generated",
    url="http://localhost:3030/pizza/query"
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