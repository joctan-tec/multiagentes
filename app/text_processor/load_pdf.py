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
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(input, convert_to_tensor=False)
        return embeddings

def save_chunks_to_chromadb(chunks, collection_name="pdf_chunks"):
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
    pdf_file_path = pathlib.Path(__file__).parent / "Codigo_Trabajo.pdf"
    chunks = process_pdf(pdf_file_path, chunk_size=500, chunk_overlap=50)
    print(f"Procesando y guardando {len(chunks)} chunks...")
    save_chunks_to_chromadb(chunks)

if __name__ == "__main__":
    main()
