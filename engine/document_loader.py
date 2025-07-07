# import os
# import tempfile
import numpy as np
import io
from typing import List, Tuple
from llama_index.core import Document
from pdf2image import convert_from_bytes
import easyocr
from PyPDF2 import PdfReader

reader = easyocr.Reader(['en', 'id'], verbose=False)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_file)
        text = "\n".join([page.extract_text() for page in reader.pages])
        return text.strip()
    except Exception:
        return ""
    
def extract_text_with_ocr(file_bytes: bytes) -> str:
    """Convert PDF pages to images and extract text using EasyOCR."""
    try:
        images = convert_from_bytes(file_bytes)
        text = ""
        for img in images:
            result = reader.readtext(np.array(img), detail=0, paragraph=True)
            text += "\n".join(result) + "\n"
        return text.strip()
    except Exception:
        return ""

def load_documents(files, session_id) -> Tuple[List[Document], str]:
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