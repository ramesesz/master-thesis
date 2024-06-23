# Run using 'python -m manon_chat_interface.scripts.embed_entities' from root
# Make sure that SPARQL server is running

import re

from manon_chat_interface.utils import sparql, vectorstore
from urllib.error import URLError

URL = "http://localhost:3030/manon/query"

# Machines ------------------------------------------------------------------------
print("Extracting machine entities...")

try:
    results = sparql.execute_sparql(url=URL, query=sparql.MACHINE_EXTRACTION_QUERY)
except URLError as e:
    print(f"\033[91mERROR. Server may not be running.\033[0m Error message: {e}")


# Extract machine names
bindings = results['results']['bindings']
machine_IRIs = [binding['individual']['value'] for binding in bindings]
machine_names = [re.split('#M_', iri)[-1] for iri in machine_IRIs]

# Embed to vectorstore
print("Embedding machine entities...")
vectorstore.embed_entities(
    path="./data/vectorstores/entities",
    collection="machine_collection",
    documents=machine_names,
    metadatas=[{"IRI": IRI} for IRI in machine_IRIs]
)

# Parts ---------------------------------------------------------------------------
print("Extracting part entities...")

try:
    results = sparql.execute_sparql(url=URL, query=sparql.PART_EXTRACTION_QUERY)
except URLError as e:
    print(f"\033[91mERROR. Server may not be running.\033[0m Error message: {e}")

# Extract part names
bindings = results['results']['bindings']
part_IRIs = [binding['individual']['value'] for binding in bindings]
part_names = [re.split('#', iri)[-1] for iri in part_IRIs]

# Embed to vectorstore
print("Embedding part entities...")
vectorstore.embed_entities(
    path="./manon_chat_interface/data/vectorstores/entities",
    collection="part_collection",
    documents=part_names,
    metadatas=[{"IRI": IRI} for IRI in part_IRIs]
)
print("All entities have been successfully embedded.")
