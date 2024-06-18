# Run using 'python -m manon_chat_interface.scripts.embed_entities' from root
# Make sure that SPARQL server is running

import re

from manon_chat_interface import utils, queries

URL = "http://localhost:3030/manon/query"

# Machines ------------------------------------------------------------------------

# Execute SPARQL query
print("Extracting machine entities...")
results = utils.execute_sparql(url=URL, query=queries.MACHINE_EXTRACTION_QUERY)

# Extract machine names
bindings = results['results']['bindings']
machine_IRIs = [binding['individual']['value'] for binding in bindings]
machine_names = [re.split('#M_', iri)[-1] for iri in machine_IRIs]

# Embed to vectorstore
print("Embedding machine entities...")
utils.embed_entities(
    path="./vectorstores/entities",
    collection="machine_collection",
    documents=machine_names,
    metadatas=[{"IRI": IRI} for IRI in machine_IRIs]
)

# Parts ---------------------------------------------------------------------------

print("Extracting part entities...")
# Execute SPARQL query
results = utils.execute_sparql(url=URL, query=queries.PART_EXTRACTION_QUERY)

# Extract part names
bindings = results['results']['bindings']
part_IRIs = [binding['individual']['value'] for binding in bindings]
part_names = [re.split('#', iri)[-1] for iri in part_IRIs]

# Embed to vectorstore
print("Embedding part entities...")
utils.embed_entities(
    path="./vectorstores/entities",
    collection="part_collection",
    documents=part_names,
    metadatas=[{"IRI": IRI} for IRI in part_IRIs]
)

print("All entities have been successfully embedded.")
