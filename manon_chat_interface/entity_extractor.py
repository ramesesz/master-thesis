import re

from SPARQLWrapper import SPARQLWrapper, JSON

# Define the SPARQL endpoint
sparql = SPARQLWrapper("http://localhost:3030/manon/query")

# Define the SPARQL query


# Execute query and return in JSON format
sparql.setQuery(query)

sparql.setReturnFormat(JSON)

results = sparql.query().convert()

# Extract machine names from query result
machine_names = [re.split('#M_', result['individual']['value'])[-1] for result in results["results"]["bindings"]]


# Todo: Embed into vectorstore