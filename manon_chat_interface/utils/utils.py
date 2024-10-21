import pandas as pd

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