from save_to_chromadb import get_chroma_client

def search(query: str, collection_name: str = "pdf_chunks", n_results: int = 5):
    """
    Search for a query in a ChromaDB collection and return results.

    Args:
        query (str): The search query.
        collection_name (str): Name of the ChromaDB collection to search in.
        n_results (int): Number of results to return.

    Returns:
        list: List of search results.
    """
    client = get_chroma_client()
    collection = client.get_collection(collection_name)

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    return results["documents"][0]



if __name__ == "__main__":
    # Example usage
    query = "Cuales son los derechos de los trabajadores?"
    results = search(query, n_results=10)
    
    print("Search results:")
    for i, doc in enumerate(results):
        print(f"{i + 1}: {doc}")