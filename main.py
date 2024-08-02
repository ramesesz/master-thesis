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
# topping_collection = entities_client.get_or_create_collection("topping_collection")

entities = orchestration.entity_recognition(original_question)["entities"] # List of entities
# recognized_pizza = entity["pizza"]
# recognized_topping = entity["topping"]
print("Entities:" + str(entities))
mapped_entities = pizza_collection.query(
    query_texts=entities,
    n_results=1
)
# TODO: Apply cosine threshold and entity not found handling.


# mapped_pizza = pizza_collection.query(
#     query_texts=recognized_pizza,
#     n_results=1
# )
# pizza_iri = mapped_pizza["metadatas"][0][0]["IRI"] # Context

# mapped_topping = topping_collection.query(
#     query_texts=recognized_topping,
#     n_results=1
# )
# topping_iri = mapped_pizza["metadatas"][0][0]["IRI"] # Context

# Get triples
triples = orchestration.get_triples(
    client=entities_client, 
    question=original_question, 
    entities=entities,
    collection_name="pizza_collection",
    mode="n_hop",
    url="http://localhost:3030/pizza/query",
    file_path="./manon_chat_interface/data/ontologies/pizza.ttl",
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
