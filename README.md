# IELTS Study Buddy

A Streamlit-based web application to assist IELTS students in practicing reading and writing skills. Upload a passage (PDF, TXT, or DOCX) to extract text, generate a summary, create interactive flashcards for vocabulary practice, and receive automated language feedback on grammar, style, and clarity.

## Features
- **Text Extraction**: Supports PDF, DOCX, and TXT files using PyMuPDF, python-docx, and basic file reading.
- **Summarization**: Generates concise summaries of passages using spaCy and TF-IDF for key sentence selection.
- **Flashcards/Quiz**: Creates interactive flashcards from named entities (e.g., people, places) with difficulty tracking.
- **Language Feedback**: Provides grammar, style, and redundancy feedback using LanguageTool, optimized for IELTS academic writing. Supports English and Arabic, with bilingual tips.
- **Streamlit UI**: User-friendly interface for uploading files, viewing results, and submitting quiz answers.

## Project Structure
```
ielts-study-assistant/
├── app.py                  # Main Streamlit app
├── lang_feedback.py        # Language feedback using LanguageTool
├── passage_utils.py        # File extraction (PDF, DOCX, TXT)
├── eng_flashcards.py       # Flashcard generation using spaCy
├── passage_summarizer.py   # Passage summarization using spaCy + TF-IDF
├── README.md              # This file
└── requirements.txt        # Dependencies (optional for deployment)
```

## Requirements
- Python 3.8+
- Dependencies (install via `pip install -r requirements.txt`):
  ```
  streamlit
  language-tool-python
  spacy
  scikit-learn
  pymupdf
  python-docx
  nltk
  ```
- spaCy model: `en_core_web_sm` (install via `python -m spacy download en_core_web_sm`)
- NLTK data: `punkt` (auto-downloaded on first run)
