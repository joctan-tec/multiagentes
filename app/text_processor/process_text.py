from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
import pathlib

def read_pdf(file_path: str) -> str:
    """
    Reads a PDF file and extracts its text content.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def clean_text(text: str) -> str:
    import re
    # Reemplaza múltiples espacios/tabs (pero conserva saltos de línea)
    text = re.sub(r'[ \t]+', ' ', text)  # Elimina espacios/tabs múltiples, pero no \n
    return text.strip()

def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list:
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
    Processes a PDF file by reading its content, cleaning the text, and splitting it into chunks.

    Args:
        file_path (str): The path to the PDF file.
        chunk_size (int): The size of each text chunk.
        chunk_overlap (int): The overlap between consecutive text chunks.

    Returns:
        list: A list of text chunks.
    """
    text = read_pdf(file_path)
    cleaned_text = clean_text(text)
    chunks = split_text(cleaned_text, chunk_size, chunk_overlap)
    return chunks
    