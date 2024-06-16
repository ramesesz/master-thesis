# run using 'python -m playground.ontology.test' from root

import re
import chromadb

from manon_chat_interface import (
    utils,
    prompts,
    queries
)
from SPARQLWrapper import SPARQLWrapper

# Execute SPARQL query
wrapper = SPARQLWrapper("http://localhost:3030/manon/query")

results = utils.execute_sparql(wrapper=wrapper, query=queries.MACHINE_EXTRACTION_QUERY)

# Extract machine names
bindings = results['results']['bindings']
machine_IRIs = [binding['individual']['value'] for binding in bindings]
machine_names = [re.split('#M_', iri)[-1] for iri in machine_IRIs]

# Create vectorstore
client = chromadb.PersistentClient(path='./vectorstores/entities')
machine_collection = client.get_or_create_collection(name="machine_collection")
machine_collection.add(
    documents=machine_names,
    ids=machine_names,
    metadatas=[{"IRI": iri} for iri in machine_IRIs]
)
