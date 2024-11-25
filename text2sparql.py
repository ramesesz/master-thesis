from manon_chat_interface.utils.sparql import *
from manon_chat_interface.utils.llm import * 
from urllib.error import HTTPError

import json
import os

# Define variables
path_to_graph = "manon_chat_interface/data/ontologies"
graph_name = "flightInstATBox.ttl"
mode = "local"
model = "Llama-3.1-8B" # This variable is for folder naming only.


def text2sparql(question, question_id):
    attempts = 0
    max_attempts = 1
    success = False
    log_data = {"attempts": []} 

    while attempts < max_attempts and not success:
        attempts += 1
        print(f"Attempt no {attempts}. Generating query...")
        attempt_info = {"attempt_number": attempts} 
        try:
            # Generate and execute SPARQL query
            gen_results = generate_sparql_query(f"{path_to_graph}/{graph_name}", question, mode)
            sparql_query = gen_results["sparql_query"]
            results = execute_sparql(url="http://localhost:3030/flight/query", query=sparql_query)
            success = True
            attempt_info["sparql_query"] = sparql_query  # Log successful SPARQL query
            attempt_info["query_explanation"] = gen_results["explanation"]
            attempt_info["query_results"] = results
            attempt_info["error"] = None 
        except HTTPError as e:
            attempt_info["sparql_query"] = gen_results["sparql_query"] if 'sparql_query' in locals() else None
            attempt_info["error"] = str(e) 
            print(f"Attempt {attempts}: Failed to execute SPARQL query due to an HTTP error - {e}")
        except Exception as e:
            attempt_info["sparql_query"] = gen_results["sparql_query"] if 'sparql_query' in locals() else None
            attempt_info["error"] = str(e) 
            print(f"Attempt {attempts}: Error - {e}")
        
        log_data["attempts"].append(attempt_info)

    log_data["number_of_attempts"] = attempts

    if not success:
        print(f"Failed after {max_attempts} attempts")

    # Save log_data to a JSON file
    print("Saving logs...")
    base_path = f"experiments/text2sparql/{graph_name}/{model}"
    file_path = os.path.join(base_path, f"{question_id}.json")

    # Ensure the directory exists
    os.makedirs(base_path, exist_ok=True)

    # Save log_data to a JSON file
    with open(file_path, "w") as json_file:
        json.dump(log_data, json_file, indent=4)


# Loop over datapoints
with open("manon_chat_interface/data/dataset/flight_dataset.json", "r") as file:
    data = json.load(file)

for index, item in enumerate(data):

    question = item["question"]
    question_id = item["id"]

    text2sparql(question=question, question_id=question_id)
