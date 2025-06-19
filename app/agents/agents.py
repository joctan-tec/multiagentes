from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.schema.messages import HumanMessage, AIMessage
from text_processor.search_chromadb import search

class AgenteBuscador:

    def ejecutar(self, pregunta):
        print("\nAgenteBuscador ejecutando...")
        fragmentos = search(pregunta, n_results=10)
        documentos = [Document(page_content=frag) for frag in fragmentos]
        return {"documentos": documentos, "pregunta": pregunta}


class AgenteAnalista:
    def __init__(self):
        self.chat = ChatOpenAI(model_name="gpt-4o-mini")

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
        self.chat = ChatOpenAI(model_name="gpt-4o-mini")

    def ejecutar(self, respuesta_analista):
        print("\nAgenteRedactor mejorando redaccion...")
        prompt = (
            f"Reescribe la siguiente respuesta en un tono claro y amigable:\n\n"
            f"{respuesta_analista}"
        )
        return {"respuesta_final": self.chat.predict(prompt)}