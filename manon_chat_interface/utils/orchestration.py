from manon_chat_interface.utils import llm
from manon_chat_interface.utils import sparql
from strictjson import strict_json

import chromadb

URL = "http://localhost:3030/pizza/query"

def entity_recognition(input: str) -> dict:
    """
    Performs entity recognition on the provided input string using a large language model (LLM).

    This function identifies and categorizes entities within the user input.

    Multiple 

    Args:
        input (str): The input string to be analyzed by the LLM.

    Returns:
        dict: A dictionary with key 'entities', containing the identified entities within the question.

    Example:
        Input: "Can Creality Ender manufacture flange?"
        Output: {'entities': ['Creality Ender', 'flange']}

    """
    response = strict_json(
        system_prompt=llm.ER_SYSTEM_PROMPT,
        user_prompt=llm.ER_USER_PROMPT.format(input=input),
        output_format={"entities": "Array of entities"},
        llm=llm.invoke_llm
    )

    return response


def get_triples(
        question: str, # Original question 
        mode: str = "default",
        path_to_vectorstore: str = "./manon_chat_interface/data/vectorstores", 
        path_to_graph: str = None, # Path to RDF graph
        format: str = None, # Format of RDF graph
):
    """Get triples to be given as context to the QA model.

    Args:
        question (str): Question.
        path_to_vectorstore (str, optional): Path to the vectorstore.
        path_to_graph (str, optional): Path to the file containing the RDF graph.

    Raises:
        ValueError: If required params not given.
        Exception: If mode is invalid.

    Returns:
        str: Text containing RDF triples.
    """

    # Get chroma. Adjust client name if necessary.
    entities_client = chromadb.PersistentClient(path=f"{path_to_vectorstore}/pizza_entities")
    questions_client = chromadb.PersistentClient(path=f"{path_to_vectorstore}/pizza_questions")

    pizza_collection = entities_client.get_or_create_collection("pizza_collection")
    question_collection = questions_client.get_or_create_collection("pizza_questions")

    # Map question
    question_emb = question_collection.query(
        query_texts=[question], 
        n_results=1
    )
    mapped_question = question_emb["documents"][0][0]

    # Map entities
    entities = entity_recognition(question)["entities"] # List of entities
    entities_emb = pizza_collection.query(
        query_texts=entities, 
        n_results=1
    )
    mapped_entities = [metadata[0]['IRI'] for metadata in entities_emb['metadatas']]

    if mode == "default":
        if path_to_graph is None or format is None:
            raise ValueError("In 'default' mode, 'path_to_graph' and 'format' cannot be None.")

        triples = sparql.load_rdf_triples(file_path=path_to_graph, format=format)
        
        return triples
    
    elif mode == "n_hop":
        # TODO: Add cases for 1, 2, 3 hops
        triples = ""
        
        for iri in mapped_entities:
            query = sparql.PREFIXES+sparql.TWO_HOP.format(IRI=iri)
            query_result = sparql.execute_parse_sparql(
                url=URL, 
                queries=[query]
            )
            triples += query_result

        return triples

    elif mode == "generated":
        # LLM Generation
        if path_to_graph is None or format is None:
            raise ValueError("In 'default' mode, 'path_to_graph' and 'format' cannot be None.")
        
        triples = sparql.load_rdf_triples(file_path=path_to_graph, format=format)

        query = strict_json(
            system_prompt=llm.CONTEXT_RETRIEVAL_SYSTEM_PROMPT.format(
                context=triples
            ),
            user_prompt=llm.CONTEXT_RETRIEVAL_USER_PROMPT.format(
                question=question
            ),
            output_format={
                "sparql_query": "Executable sparql query string.", 
                "explanation": "Explanation of what the sparql query does."
            },
            llm=llm.invoke_llm
        )
        # try:
        #     response = sparql.execute_parse_sparql(url, [query])
        
        # except Exception as e:
        #     print(f"The following error occured when executing generated query:/n{e}")
        
        return query
    
    else:
        raise Exception("Given mode is not valid. Choose between 'default', 'n-hop', or 'generated'")


