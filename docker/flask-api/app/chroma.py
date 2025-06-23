import chromadb

class ChromaDBClient:
    """
    Clase para manejar la conexión y búsqueda en ChromaDB.
    """

    def __init__(self, host="chroma", port=8000):
        """
        Inicializa el cliente de ChromaDB.
        Args:
            host (str): Host donde se encuentra ChromaDB.
            port (int): Puerto de conexión.
        """
        self.client = chromadb.HttpClient(host=host, port=port)

    def search(self, query: str, collection_name: str = "pdf_chunks", n_results: int = 5):
        """
        Realiza una búsqueda en la colección de ChromaDB y devuelve los fragmentos de texto más relevantes.
        Args:
            query (str): Consulta de búsqueda.
            collection_name (str): Nombre de la colección en ChromaDB donde se almacenan los fragmentos.
            n_results (int): Número de resultados a devolver.
        Returns:
            list: Lista de fragmentos de texto más relevantes encontrados en la colección.
        """
        collection = self.client.get_collection(collection_name)
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
        )
        return results["documents"][0]