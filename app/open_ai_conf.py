from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

load_dotenv()

class Config:

    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not self.OPENAI_API_KEY:
            raise ValueError("La clave de API de OpenAI no está configurada. Por favor, establece la variable de entorno 'OPEN_AI_API_KEY'.")
        self.openai_client = OpenAI(api_key=self.OPENAI_API_KEY)

    def configurar_entorno(self):
        os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY

    def crear_retriever(self):
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma(persist_directory="./chromadb", embedding_function=embeddings)
        return vectorstore.as_retriever()