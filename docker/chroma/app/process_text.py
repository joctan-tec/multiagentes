from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
import pathlib

def read_pdf(file_path: str) -> str:
    """
    Lee el contenido de un archivo PDF y devuelve el texto extraído.
    Args:
        file_path (str): La ruta al archivo PDF.
    Returns:
        str: El texto extraído del PDF.
    """
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def clean_text(text: str) -> str:
    """
    Limpia el texto extraído del PDF eliminando espacios y tabs innecesarios.
    Args:
        text (str): El texto extraído del PDF.
    Returns:
        str: El texto limpio.
    """
    import re
    # Reemplaza múltiples espacios/tabs (pero conserva saltos de línea)
    text = re.sub(r'[ \t]+', ' ', text)  # Elimina espacios/tabs múltiples, pero no \n
    return text.strip()

def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list:
    """
    Divide el texto en chunks de tamaño específico con superposición.
    Args:
        text (str): El texto a dividir.
        chunk_size (int): El tamaño de cada chunk.
        chunk_overlap (int): La cantidad de superposición entre chunks consecutivos.
    Returns:
        list: Una lista de chunks de texto.
    """
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separator="\n",  # Fuerza a dividir por saltos de línea
        keep_separator=True  # Mantiene el separador en los chunks
    )
    return text_splitter.split_text(text)

def process_pdf(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    """
    Procesa un archivo PDF, extrae su texto, lo limpia y lo divide en chunks.
    Args:
        file_path (str): La ruta al archivo PDF.
        chunk_size (int): El tamaño de cada chunk de texto.
        chunk_overlap (int): La cantidad de superposición entre chunks consecutivos.
    Returns:
        list: Una lista de chunks de texto procesados.
    """
    text = read_pdf(file_path)
    cleaned_text = clean_text(text)
    chunks = split_text(cleaned_text, chunk_size, chunk_overlap)
    return chunks
    