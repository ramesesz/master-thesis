from manon_chat_interface.utils import llm
from manon_chat_interface.utils import sparql
from strictjson import strict_json

import chromadb


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
        client: chromadb.PersistentClient, 
        question: str, 
        entities: list, 
        collection_name: str, 
        mode: str = "default", 
        url: str = "http://localhost:3030/pizza/query", 
        file_path: str = None, 
        format: str = None
):
    """Helper function for retrieve_context()

    Args:
        client (chromadb.PersistentClient): Chroma client.
        entities (list(str)): Entity being queried to chroma.
        collection_name (str): Chromadb collection.
        mode (str): Mode of context retrieval.
        url (str): LM Studio URL.
        file_path (str): Path to turtle file.

    Returns:
        str: SPARQL query.
    """
    if entities:
        if mode == "default":
            if file_path is None or format is None:
                raise ValueError("In 'default' mode, 'file_path' and 'format' cannot be None.")

            triples = sparql.load_rdf_triples(file_path=file_path, format=format)
            
            return triples
        
        elif mode == "n_hop":
            # TODO: Add cases for 1, 2, 3 hops
            if client is None or collection_name is None:
                raise ValueError("In 'n_hop' mode, 'client' and 'collection_name' cannot be None.")
                        
            collection = client.get_or_create_collection(collection_name)
            embeddings = collection.query(query_texts=entities, n_results=1)
            iris = [metadata[0]['IRI'] for metadata in embeddings['metadatas']]
            
            triples = ""
            
            for iri in iris:
                query = sparql.PREFIXES+sparql.TWO_HOP.format(IRI=iri)
                query_result = sparql.execute_parse_sparql(
                    url=url, 
                    queries=[query]
                )
                triples += query_result

            return triples

        elif mode == "generated":
            # LLM Generation

            # Get context using default mode
            queries = [sparql.ALL_TRIPLES_QUERY]
            context = sparql.execute_parse_sparql(url, queries)

            # Generate query using context from default mode
            # query = llm.invoke_llm(
            #     system_prompt=llm.CONTEXT_RETRIEVAL_SYSTEM_PROMPT.format(
            #         context=context
            #     ),
            #     user_prompt=llm.CONTEXT_RETRIEVAL_USER_PROMPT.format(
            #         question=question
            #     )
            # )

            query = strict_json(
                system_prompt=llm.CONTEXT_RETRIEVAL_SYSTEM_PROMPT.format(
                    context=context
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
    
    else:
        raise Exception("No entity is recognized from given question.")


# TODO: What is this for again?
def retrieve_context(entities: dict, # From entity recognition
                     question: str, # From question
                     path: str, # Path to vectorstore
                     mode: str = "default", 
                     url: str = "http://localhost:3030/pizza/query"
                     ):
    try:
        client = chromadb.PersistentClient(path=path)
        pizza_info = get_triples(client, question, entities.get("pizza"), "pizza_collection", mode, url)
        topping_info = get_triples(client, question, entities.get("topping"), "topping_collection", mode, url)
        return {
            "pizza": pizza_info,
            "topping": topping_info
        }
    except Exception as e:
        print(f"An error occurred when retrieving context: {e}")
        return None
