from manon_chat_interface.utils.sparql import *
from manon_chat_interface.utils.llm import * 

import json
import os

# Define variables
mode = "huggingface"
model = "Llama-3.1-70B" # This variable is for folder naming only.

def triple2text(question, question_id, triples, mode):
    if mode=="huggingface":
        gen_results = invoke_huggingface(
            system_prompt=TRIPLE2TEXT_SYSTEM_PROMPT.format(triples=triples),
            user_prompt=TRIPLE2TEXT_USER_PROMPT.format(question=question)
        )
    else:
        gen_results = invoke_llm(
            system_prompt=TRIPLE2TEXT_SYSTEM_PROMPT.format(triples=triples),
            user_prompt=TRIPLE2TEXT_USER_PROMPT.format(question=question)        
        )

    # Define the path for saving the results
    base_path = f"experiments/triple2text/{model}"
    os.makedirs(base_path, exist_ok=True)
    file_path = os.path.join(base_path, f"{question_id}.json")

    output_data = {
        "gen_results": gen_results
    }

    # Save the generated results to a JSON file
    with open(file_path, "w") as json_file:
        json.dump(output_data, json_file, indent=4)
    print(f"Results for question ID {question_id} saved to {file_path}")

# Loop over datapoints
with open("manon_chat_interface/data/dataset/flight_dataset.json", "r") as file:
    data = json.load(file)

for index, item in enumerate(data):
    if index==3: break
    question = item["question"]
    question_id = item["id"]
    triples = item["triples"]

    triple2text(question=question, 
                question_id=question_id, 
                triples=triples,
                mode=mode)
