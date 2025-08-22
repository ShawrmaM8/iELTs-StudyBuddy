# Purpose: Handle file reading (with optional translation, PDF reading)

import fitz  # PyMuPDF
from docx import Document
import nltk
from nltk.tokenize import sent_tokenize

# Ensure required NLTK resources are available
def setup_nltk():
    resources = ["punkt", "stopwords"]
    for resource in resources:
        try:
            nltk.data.find(f"tokenizers/{resource}" if resource == "punkt" else f"corpora/{resource}")
        except LookupError:
            nltk.download(resource, quiet=True)

setup_nltk()

def extract_text(file):
    """Detect file type and extract text from PDF, DOCX, or plain text files."""
    if file.type == 'application/pdf':
        return extract_text_from_pdf(file)
    elif file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return extract_text_from_docx(file)
    elif file.type == 'text/plain':
        return file.read().decode('utf-8')
    else:
        raise ValueError(f"Unsupported file type: {file.type}")

def extract_text_from_pdf(file):
    """Extract text from a PDF file using PyMuPDF."""
    doc = fitz.open(stream=file.read(), filetype='pdf')
    text = ''
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    """Extract text from a DOCX file using python-docx."""
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def split_sentences(text):
    """Split text into sentences using NLTK's sentence tokenizer."""
    return sent_tokenize(text)

