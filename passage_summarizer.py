# Purpose: Passage summarization logic using spaCy + TF-IDF

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import string

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


def summarize_text(text, num_sentences=3):
    """
    Extractive text summarization using NLTK
    """
    try:
        # Tokenize into sentences
        sentences = sent_tokenize(text)
        if len(sentences) <= num_sentences:
            return sentences

        # Clean and tokenize words
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english') + list(string.punctuation))
        filtered_words = [word for word in words if word not in stop_words and word.isalnum()]

        # Calculate word frequencies
        word_freq = FreqDist(filtered_words)

        # Score sentences based on word frequencies
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            sentence_words = word_tokenize(sentence.lower())
            score = sum(word_freq[word] for word in sentence_words if word in word_freq)
            sentence_scores[i] = score

        # Get top sentences
        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        summary = [sentences[i] for i in sorted(top_sentences)]

        return summary

    except Exception as e:
        return [f"Summarization error: {str(e)}"]