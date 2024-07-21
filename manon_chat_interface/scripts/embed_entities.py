# Run using 'python -m manon_chat_interface.scripts.embed_entities' from root
# Make sure that SPARQL server is running

import re

from manon_chat_interface.utils.sparql import *
from manon_chat_interface.utils import vectorstore
from urllib.error import URLError

URL = "http://localhost:3030/pizza/query"

# Machines ------------------------------------------------------------------------
print("Extracting pizzas...")

try:
    iri = "pizza:Pizza"
    results = execute_sparql(url=URL, query=PREFIXES+EXTRACTION_QUERY.format(pizza_class=iri))
except URLError as e:
    print(f"\033[91mERROR. Server may not be running.\033[0m Error message: {e}")


# Extract names
bindings = results['results']['bindings']
pizza_IRIs = [binding['individual']['value'] for binding in bindings]
pizza_names = [re.split('#', iri)[-1] for iri in pizza_IRIs]

# Embed to vectorstore
print("Embedding pizzas...")
vectorstore.embed_entities(
    path="./manon_chat_interface/data/vectorstores/pizza_entities",
    collection="pizza_collection",
    documents=pizza_names,
    metadatas=[{"IRI": IRI} for IRI in pizza_IRIs]
)

# Parts ---------------------------------------------------------------------------
print("Extracting toppings...")

try:
    iri = "pizza:PizzaTopping"
    results = execute_sparql(url=URL, query=PREFIXES+EXTRACTION_QUERY.format(pizza_class=iri))
except URLError as e:
    print(f"\033[91mERROR. Server may not be running.\033[0m Error message: {e}")

# Extract part names
bindings = results['results']['bindings']
part_IRIs = [binding['individual']['value'] for binding in bindings]
part_names = [re.split('#', iri)[-1] for iri in part_IRIs]

# Embed to vectorstore
print("Embedding toppings...")
vectorstore.embed_entities(
    path="./manon_chat_interface/data/vectorstores/pizza_entities",
    collection="topping_collection",
    documents=part_names,
    metadatas=[{"IRI": IRI} for IRI in part_IRIs]
)
print("All entities have been successfully embedded.")
