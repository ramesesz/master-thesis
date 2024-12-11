# Run using 'python -m manon_chat_interface.scripts.embed_entities' from root
# Make sure that SPARQL server is running

import sys
import os
import pandas as pd
from manon_chat_interface.utils.sparql import *
from manon_chat_interface.utils import vectorstore
from dotenv import load_dotenv

load_dotenv()
SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT')

# Define the query exactly as in the first script
query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT DISTINCT ?classIRI ?classLabel ?classComment ?entity ?entityLabel ?entityComment
WHERE {
    {
        ?classIRI a owl:Class .
        OPTIONAL { ?classIRI rdfs:label ?classLabel . }
        OPTIONAL { ?classIRI rdfs:comment ?classComment . }
    }
    UNION
    {
        ?entity a ?classIRI .
        ?classIRI a owl:Class .
        OPTIONAL { ?entity rdfs:label ?entityLabel . }
        OPTIONAL { ?entity rdfs:comment ?entityComment . }
    }
}
"""

print("Executing query...")
results = execute_sparql(url=SPARQL_ENDPOINT, query=query)

print("Parsing results...")
classes_data = []
entities_data = []

# Process the JSON results as needed to populate the data lists
for item in results['results']['bindings']:
    classIRI = item.get('classIRI', {}).get('value', None)
    classLabel = item.get('classLabel', {}).get('value', None)
    classComment = item.get('classComment', {}).get('value', "")
    entity = item.get('entity', {}).get('value', None)
    entityLabel = item.get('entityLabel', {}).get('value', None)
    entityComment = item.get('entityComment', {}).get('value', "")

    if entity is None:
        if classIRI and classLabel:
            classes_data.append({
                "iri": classIRI,
                "label": classLabel,
                "comment": classComment
            })
    else:
        if entity and entityLabel: 
            entities_data.append({
                "iri": entity,
                "label": entityLabel,
                "comment": entityComment
            })

classes_df = pd.DataFrame(classes_data)
entities_df = pd.DataFrame(entities_data)

df = pd.concat([classes_df, entities_df], ignore_index=True)

# This filtering is knowledge graph specific in order to optimize embedding search.
# When given flight codes, the routes are deemed more similar than the flight label itself.
df = df[~df['label'].str.contains('Planned Route|Actual Route', na=False)]

labels = df['label'].tolist()
iris = df['iri'].tolist()
comments = df['comment'].tolist()

print("Embedding...")
metadatas = [{"iri": iri, "comments": comment} for iri, comment in zip(iris, comments)]

vectorstore.embed_entities(
    path="./manon_chat_interface/data/vectorstores/flight_vectorstore",
    collection="flight_collection",
    documents=labels,
    metadatas=metadatas
)
