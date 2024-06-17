# run using 'python -m playground.ontology.test' from root

import re
import chromadb

from manon_chat_interface import (
    utils,
    queries
)

URL = "http://localhost:3030/manon/query"

# Extract Machines ------------------------------------------------------------------------

# Execute SPARQL query
results = utils.execute_sparql(url=URL, query=queries.MACHINE_EXTRACTION_QUERY)

# Extract machine names
bindings = results['results']['bindings']
machine_IRIs = [binding['individual']['value'] for binding in bindings]
machine_names = [re.split('#M_', iri)[-1] for iri in machine_IRIs]

# Embed to vectorstore
utils.embed_entities(
    path="./vectorstores/entities",
    collection="machine_collection",
    documents=machine_names,
    iris=machine_IRIs
)

# Extract Parts ------------------------------------------------------------------------

# Execute SPARQL query
results = utils.execute_sparql(url=URL, query=queries.PART_EXTRACTION_QUERY)

# Extract part names
bindings = results['results']['bindings']
part_IRIs = [binding['individual']['value'] for binding in bindings]
part_names = [re.split('#', iri)[-1] for iri in part_IRIs]

# Embed to vectorstore
utils.embed_entities(
    path="./vectorstores/entities",
    collection="part_collection",
    documents=part_names,
    iris=part_IRIs
)

