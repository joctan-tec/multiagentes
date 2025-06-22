from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.schema.messages import HumanMessage, AIMessage
import chromadb

def get_chroma_client():
    """
    Initialize and return a ChromaDB client.
    """
    return chromadb.HttpClient(
        host="chroma",
        port=8000,
    )

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


class AgenteBuscador:

    def ejecutar(self, pregunta):
        print("\nAgenteBuscador ejecutando...")
        fragmentos = search(pregunta, n_results=10)
        documentos = [Document(page_content=frag) for frag in fragmentos]
        return {"documentos": documentos, "pregunta": pregunta}


class AgenteAnalista:
    def __init__(self):
        self.chat = ChatOpenAI(model_name="gpt-4o")

    def ejecutar(self, documentos, pregunta, respuesta_anterior=None):
        print("\nAgenteAnalista procesando...")
        contexto = "\n".join([doc.page_content for doc in documentos])

        mensajes = []
        if respuesta_anterior:
            mensajes.append(AIMessage(content=respuesta_anterior))
        mensajes.append(HumanMessage(content=(
            f"Con base en los siguientes textos legales:\n{contexto}\n\n"
            f"Responde claramente a la pregunta:\n{pregunta}"
        )))

        respuesta = self.chat.invoke(mensajes)
        return {"respuesta_analista": respuesta.content}


class AgenteRedactor:
    def __init__(self):
        self.chat = ChatOpenAI(model_name="gpt-4o")

    def ejecutar(self, respuesta_analista):
        print("\nAgenteRedactor mejorando redaccion...")
        prompt = (
            f"Reescribe la siguiente respuesta en un tono claro y amigable además, devuelve la respuesta en formato Markdown válido, sin caracteres escapados:\n\n"
            f"{respuesta_analista}"
        )
        return {"respuesta_final": self.chat.predict(prompt)}