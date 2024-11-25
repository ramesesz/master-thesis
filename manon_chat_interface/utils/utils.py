from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer
import bert_score
import pandas as pd


def calculate_bleu(generated_text, golden_text):
    reference = [golden_text.split()]
    candidate = generated_text.split()
    bleu_score = sentence_bleu(reference, candidate)
    return bleu_score

def calculate_rouge_n(generated_text, golden_text, n=1):
    scorer = rouge_scorer.RougeScorer([f'rouge{n}'], use_stemmer=True)
    scores = scorer.score(golden_text, generated_text)
    rouge_n_score = scores[f'rouge{n}'].fmeasure  # F1 measure for ROUGE-N
    return rouge_n_score

def calculate_meteor(generated_text, golden_text):
    meteor = meteor_score([golden_text.split()], generated_text.split())
    return meteor

def calculate_bert_score(generated_text, golden_text, model_type="bert-base-uncased"):
    P, R, F1 = bert_score.score([generated_text], [golden_text], model_type=model_type)
    bert_f1 = F1.item()  # Return F1 as the main BERTScore
    return bert_f1

def replace_urls_with_prefixes(text, prefix_dict):
    """Replace URLs with prefixes in a given string.

    Args:
        text (str): String containing SPARQL query or text.
        prefix_dict (dict): Mapping of prefixes to URLs.
    """
    for prefix, url in prefix_dict.items():
        text = text.replace(url, prefix)
    return text


def replace_prefixes_with_urls(text, prefix_dict):
    """Replace prefixes with URLs in a given string.

    Args:
        text (str): String containing SPARQL query or text.
        prefix_dict (dict): Mapping of prefixes to URLs.
    """
    for prefix, url in prefix_dict.items():
        text = text.replace(prefix, url)
    return text


def parse_sparql_output(query_output: dict):
    """Parse query JSON output to dataframe.

    Args:
        query_output (dict): The output from a SPARQL query in JSON format

    Returns:
        pd.DataFrame: the parsed results as a pandas DataFrame
    """
    columns = query_output['head']['vars']
    rows = []
    for result in query_output['results']['bindings']:
        row = {}
        for col in columns:
            row[col] = result[col]['value'] if col in result else None
        rows.append(row)
    df = pd.DataFrame(rows, columns=columns)
    return df