# Purpose: Handle file reading (with optional translation, PDF reading)

import fitz
import docx
import io

def extract_text(file):
    """Detect file type and extract text with error handling"""
    try:
        if file.type == 'application/pdf':
            return extract_text_from_pdf(file)
        elif file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return extract_text_from_docx(file)
        elif file.type == 'text/plain':
            return file.read().decode('utf-8')
        else:
            raise ValueError("Unsupported file type")
    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")

def extract_text_from_pdf(file):
    """Extract text from PDF using pymupdf"""
    try:
        # Reset file pointer to beginning
        file.seek(0)
        file_bytes = file.read()
        doc = fitz.open(stream=file_bytes, filetype='pdf')
        text = ''
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        file.seek(0)
        doc = docx.Document(io.BytesIO(file.read()))
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        raise Exception(f"DOCX extraction failed: {str(e)}")