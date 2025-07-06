# import os
# import tempfile
from typing import List, Tuple
from llama_index.core import Document
from pdf2image import convert_from_bytes
import pytesseract
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        reader = PdfReader(file_bytes)
        text = "\n".join([page.extract_text() for page in reader.pages])
        return text.strip()
    except:
        return ""
    
def extract_text_with_ocr(file_bytes:bytes) -> str:
    images = convert_from_bytes(file_bytes)
    text = "\n".join([pytesseract.image_to_string(image) for image in images])
    return text.strip()

def load_document(files, session_id) -> Tuple[List[Document], str]:
    documents = []
    previews = []

    for file in files:
        file_bytes = file.read()
        text = extract_text_from_pdf(file_bytes)

        if not text:
            text = extract_text_with_ocr(file_bytes)

        doc = Document(
            text=text,
            metadata={"source": file.name, "doc_id": f"{session_id}-{file.name}"}
        )
        documents.append(doc)
        previews.append(file_bytes)
    
    return documents, previews