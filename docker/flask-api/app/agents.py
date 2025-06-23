from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.schema.messages import HumanMessage, AIMessage
from chromadb import ChromaDBClient

class AgenteBuscador:
    '''
    Agente encargado de buscar fragmentos relevantes en la base de datos ChromaDB.
    '''
    def ejecutar(self, pregunta):
        """
        Ejecuta el agente buscador para encontrar fragmentos relevantes en ChromaDB.
        Args:
            pregunta (str): Pregunta o consulta que el agente debe buscar.
        Returns:
            dict: Diccionario con los documentos encontrados y la pregunta original.
        """
        print("\nAgenteBuscador ejecutando...")
        fragmentos = ChromaDBClient().search(pregunta, n_results=10)
        documentos = [Document(page_content=frag) for frag in fragmentos]
        return {"documentos": documentos, "pregunta": pregunta}


class AgenteAnalista:
    '''
    Agente encargado de analizar los fragmentos legales y responder a la pregunta.
    Este agente utiliza el modelo GPT-4o de OpenAI para generar respuestas basadas en los documentos proporcionados.
    '''
    def __init__(self):
        self.chat = ChatOpenAI(model_name="gpt-4o")

    def ejecutar(self, documentos, pregunta, respuesta_anterior=None):
        """
        Ejecuta el agente analista para procesar los documentos y responder a la pregunta.
        Args:
            documentos (list): Lista de documentos relevantes encontrados por el agente buscador.
            pregunta (str): Pregunta que se debe responder.
            respuesta_anterior (str, optional): Respuesta previa del analista para continuar el flujo.
        Returns:
            dict: Diccionario con la respuesta generada por el agente analista.
        """
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
    '''
    Agente encargado de mejorar la redacción de la respuesta del analista.
    Este agente utiliza el modelo GPT-4o de OpenAI para reescribir la respuesta en un tono claro y amigable.
    '''
    def __init__(self):
        self.chat = ChatOpenAI(model_name="gpt-4o")

    def ejecutar(self, respuesta_analista):
        """
        Ejecuta el agente redactor para mejorar la redacción de la respuesta del analista.
        Args:
            respuesta_analista (str): Respuesta generada por el agente analista.
        Returns:
            dict: Diccionario con la respuesta final mejorada en formato Markdown.
        """
        print("\nAgenteRedactor mejorando redaccion...")
        prompt = (
            f"Reescribe la siguiente respuesta en un tono claro y amigable además, devuelve la respuesta en formato Markdown válido, sin caracteres escapados:\n\n"
            f"{respuesta_analista}"
        )
        return {"respuesta_final": self.chat.predict(prompt)}
