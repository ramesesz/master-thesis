from manon_chat_interface import utils

QUESTIONS_LIST = [
    "Which machines can manufacture my part?",
    "Which manufacturing process can be used to manufacture my part?",
    "What do I have to change in order to be able to produce my part on machine x?",
    "What do I have to change in order to be able to produce my part with manufacturing process x?",
]

# Embed to vectorstore
print("Embedding questions...")
utils.embed_entities(
    path="./vectorstores/competency_questions",
    collection="competency_questions",
    documents=QUESTIONS_LIST,
)

print("All entities have been successfully embedded.")
