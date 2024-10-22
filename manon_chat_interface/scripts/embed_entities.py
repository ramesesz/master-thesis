# Run using 'python -m manon_chat_interface.scripts.embed_entities' from root
# Make sure that SPARQL server is running

import re
import os

from manon_chat_interface.utils.sparql import *
from manon_chat_interface.utils import vectorstore
from dotenv import load_dotenv

load_dotenv()
SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT')

# Extract entities
print("Extracting entities...")

iri = "pizza:Pizza"
results = execute_sparql(url=SPARQL_ENDPOINT, query=PREFIXES+EXTRACTION_QUERY.format(pizza_class=iri))

bindings = results['results']['bindings']
pizza_IRIs = [binding['individual']['value'] for binding in bindings]
pizza_names = [re.split('#', iri)[-1] for iri in pizza_IRIs]

iri = "pizza:PizzaTopping"
results = execute_sparql(url=SPARQL_ENDPOINT, query=PREFIXES+EXTRACTION_QUERY.format(pizza_class=iri))

bindings = results['results']['bindings']
topping_IRIs = [binding['individual']['value'] for binding in bindings]
topping_names = [re.split('#', iri)[-1] for iri in topping_IRIs]

# Embed to vectorstore
print("Embedding entities...")
vectorstore.embed_entities(
    path="./manon_chat_interface/data/vectorstores/pizza_entities",
    collection="pizza_entities_collection",
    documents=pizza_names+topping_names,
    metadatas=[{"IRI": IRI} for IRI in pizza_IRIs+topping_IRIs]
)

print("All entities have been successfully embedded.")
