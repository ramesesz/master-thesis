from manon_chat_interface.utils.sparql import *
from manon_chat_interface.utils.llm import * 
from manon_chat_interface.utils.utils import * 

import json
import os

# Define variables
mode = "local"
model = "Llama-3.1-8B" # This variable is for folder naming only.

def triple2text(question, question_id, triples, answer, mode):
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

    # Calculate metrics
    bleu = calculate_bleu(gen_results, answer)
    rouge_1 = calculate_rouge_n(gen_results, answer, n=1)
    rouge_2 = calculate_rouge_n(gen_results, answer, n=2)
    meteor = calculate_meteor(gen_results, answer)
    BERTscore = calculate_bert_score(gen_results, answer)

    output_data = {
        "gen_results": gen_results,
        "answer": answer,
        "bleu": bleu,
        "rouge_1": rouge_1,
        "rouge_2": rouge_2,
        "meteor": meteor,
        "BERTscore": BERTscore
    }

    # Save the generated results to a JSON file
    with open(file_path, "w") as json_file:
        json.dump(output_data, json_file, indent=4)
    print(f"Results for question ID {question_id} saved to {file_path}")

# Loop over datapoints
with open("manon_chat_interface/data/dataset/flight_dataset.json", "r") as file:
    data = json.load(file)

for index, item in enumerate(data):
    question = item["question"]
    question_id = item["id"]
    triples = item["triples"]
    answer = item["answer"]

    triple2text(question=question, 
                question_id=question_id, 
                triples=triples,
                answer=answer,
                mode=mode)
