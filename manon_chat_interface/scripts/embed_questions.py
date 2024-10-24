# This script is deprecated as it is part of an old architecture design.
# Run using 'python -m manon_chat_interface.scripts.embed_questions' from root

from manon_chat_interface.utils import vectorstore

QUESTIONS_LIST = [
    # "Which machines can manufacture my part?",
    # "Which manufacturing process can be used to manufacture my part?",
    # "What do I have to change in order to be able to produce my part on machine x?",
    # "What do I have to change in order to be able to produce my part with manufacturing process x?",
    "Do I need this particular topping for my pizza?"
]

# Embed to vectorstore
print("Embedding questions...")
vectorstore.embed_entities(
    path="./manon_chat_interface/data/vectorstores/pizza_questions",
    collection="pizza_questions_collection",
    documents=QUESTIONS_LIST,
)

print("All questions have been successfully embedded.")
