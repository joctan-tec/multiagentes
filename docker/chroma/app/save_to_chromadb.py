import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from text_processor.process_text import process_pdf  # Return list of text chunks from PDF
import pathlib
import json
from typing import List

def get_chroma_client():
    return chromadb.HttpClient(
        host="localhost",
        port=8000,
    )

class MyEmbeddingFunction:
    """
    Custom embedding function using SentenceTransformer for ChromaDB.
    This class is used to create a custom embedding function that ChromaDB can use.
    """
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        # Convert the input to embeddings
        embeddings = self.model.encode(input, convert_to_tensor=False).tolist()
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

    # Add documents to the collection
    collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )
    print(f"Added {len(chunks)} chunks to the collection '{collection_name}'.")

def main():
    """
    Función principal para procesar un archivo PDF, dividirlo en chunks y guardarlos en ChromaDB.
    """
    print("Processing PDF file and saving chunks to ChromaDB...")
    # Path to the PDF file
    pdf_file_path = "Codigo_Trabajo.pdf"  # Update with your PDF file path
    pdf_file_path = pathlib.Path(__file__).parent / pdf_file_path
    
    print(f"PDF file path: {pdf_file_path}")

    # Process the PDF file to get text chunks
    chunks = process_pdf(pdf_file_path, chunk_size=500, chunk_overlap=50)
    
    print(f"Number of chunks created: {len(chunks)}")

    # Save the chunks to ChromaDB
    save_chunks_to_chromadb(chunks)
    
    print(f"Saved {len(chunks)} chunks to ChromaDB collection.")
    print("Done.")
    print("Example query: 'Cuales son los derechos de los trabajadores?'")
    client = get_chroma_client()
    collection = client.get_collection("pdf_chunks")
    results = collection.query(
        query_texts=["Cuales son los derechos de los trabajadores?"],
        n_results=5,
    )
    print("Query results:")
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()