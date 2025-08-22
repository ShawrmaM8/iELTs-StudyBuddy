# Purpose: Passage summarization logic using spaCy + TF-IDF

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

nlp = spacy.load('en_core_web_sm')

def summarize_text(text, top_n=3):
    """Return top_n sentences based on TF-IDF scores with improved preprocessing."""
    # Use spaCy for better sentence segmentation
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 0]
    
    if len(sentences) <= top_n:
        return sentences
    
    # Filter out very short sentences and improve preprocessing
    filtered_sentences = [sent for sent in sentences if len(sent.split()) >= 3]
    
    if not filtered_sentences:
        return sentences[:top_n]
    
    # Use TF-IDF with better parameters
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=1000,
        ngram_range=(1, 2)  # Include bigrams
    )
    
    try:
        X = vectorizer.fit_transform(filtered_sentences)
        scores = np.array(X.sum(axis=1)).ravel()
        top_indices = scores.argsort()[-top_n:][::-1]
        
        # Return sentences in original order for better coherence
        summary_sentences = [filtered_sentences[i] for i in sorted(top_indices)]
        return summary_sentences
        
    except Exception:
        # Fallback to first sentences if TF-IDF fails
        return sentences[:top_n]