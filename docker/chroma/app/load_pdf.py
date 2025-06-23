import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List
import pathlib
import json
from process_text import process_pdf  # Import the function to process PDF files

def get_chroma_client():
    return chromadb.HttpClient(host="localhost", port=8000)

class MyEmbeddingFunction:
    """
    Clase para generar embeddings de texto utilizando SentenceTransformer.
    Esta clase se utiliza para crear una función de embedding personalizada que ChromaDB puede usar.
    """
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(input, convert_to_tensor=False)
        return embeddings

def save_chunks_to_chromadb(chunks, collection_name="pdf_chunks"):
    """
    Guarda los chunks de texto en una colección de ChromaDB.
    Args:
        chunks (List[str]): Lista de fragmentos de texto a guardar.
        collection_name (str): Nombre de la colección en ChromaDB donde se almacenarán los fragmentos.
    """
    client = get_chroma_client()
    embedding_function = MyEmbeddingFunction()

    try:
        collection = client.get_collection(collection_name)
        print(f"Using existing collection: {collection_name}")
    except chromadb.errors.NotFoundError:
        print(f"Creating new collection: {collection_name}")
        collection = client.create_collection(
            name=collection_name,
            embedding_function=embedding_function,
            metadata={"description": "Collection of PDF text chunks"}
        )

    collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )
    print(f"Added {len(chunks)} chunks to the collection '{collection_name}'.")

def main():
    """
    Función principal para cargar PDFs desde un directorio, procesarlos en chunks y guardarlos en ChromaDB.
    """
    pdf_dir = pathlib.Path(__file__).parent / "dataset"
    if not pdf_dir.exists() or not pdf_dir.is_dir():
        print(f"Error: El directorio '{pdf_dir}' no existe.")
        return
    pdf_paths = list(pdf_dir.glob("*.pdf"))  # Todos los PDFs en la carpeta
    if not pdf_paths:
        print(f"No se encontraron archivos PDF en el directorio '{pdf_dir}'.")
        return

    todos_los_chunks = []
    
    for pdf_path in pdf_paths:
        print(f"Procesando: {pdf_path.name}")
        chunks = process_pdf(pdf_path, chunk_size=500, chunk_overlap=50)
        todos_los_chunks.extend(chunks)

    print(f"\nGuardando un total de {len(todos_los_chunks)} chunks en ChromaDB...")
    save_chunks_to_chromadb(todos_los_chunks)
    print("Proceso completado.")

if __name__ == "__main__":
    main()
