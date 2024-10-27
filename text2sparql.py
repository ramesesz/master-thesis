from manon_chat_interface.utils.sparql import *
from manon_chat_interface.utils.llm import * 
from dotenv import load_dotenv
from urllib.error import HTTPError

import json
import os

# Set variables
# Change env for local and online settings
load_dotenv(dotenv_path=".env", override=True)
SPARQL_ENDPOINT = os.getenv("SPARQL_ENDPOINT")
LLM_MODEL = os.getenv("LLM_MODEL")
LLM_ENDPOINT = os.getenv("LLM_ENDPOINT")
API_KEY = os.getenv("API_KEY")

path_to_graph = "manon_chat_interface/data/ontologies/flightInstATBox.ttl"
question = "Which flight took off first, AAL1102 or ACA722?"
question_id = 1

# Define variables
attempts = 0
max_attempts = 1
success = False
log_data = {"attempts": []} 

while attempts < max_attempts and not success:
    print(f"Attempt no {attempts}. Generating query...")
    attempt_info = {"attempt_number": attempts + 1}  # Store the current attempt number
    try:
        # Generate and execute SPARQL query
        results = generate_sparql_query(path_to_graph, question)
        sparql_query = results["sparql_query"]
        execute_sparql(url=SPARQL_ENDPOINT, query=sparql_query)
        success = True
        attempt_info["sparql_query"] = sparql_query  # Log successful SPARQL query
        attempt_info["error"] = None 
    except HTTPError as e:
        attempts += 1
        attempt_info["sparql_query"] = sparql_query if 'sparql_query' in locals() else None
        attempt_info["error"] = str(e) 
        print(f"Attempt {attempts}: Failed to execute SPARQL query due to an HTTP error - {e}")
    except Exception as e:
        attempts += 1
        attempt_info["sparql_query"] = sparql_query if 'sparql_query' in locals() else None
        attempt_info["error"] = str(e) 
        print(f"Attempt {attempts}: Error - {e}")
    
    log_data["attempts"].append(attempt_info)

log_data["number_of_attempts"] = attempts

if not success:
    print(f"Failed after {max_attempts} attempts")

# Save log_data to a JSON file
print("Saving logs...")
base_path = f"evaluation/text2sparql/{LLM_MODEL}"
file_path = os.path.join(base_path, f"{question_id}.json")

# Ensure the directory exists
os.makedirs(base_path, exist_ok=True)

# Save log_data to a JSON file
with open(file_path, "w") as json_file:
    json.dump(log_data, json_file, indent=4)
