# Purpose: Generate flashcards from extracted text using spaCy-named entities

import re
import random
from collections import defaultdict


def generate_flashcards(text):
    """
    Generate flashcards from text using pattern matching
    """
    try:
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

        flashcards = []

        # Question patterns
        patterns = [
            (r'\b(?:what|which)\b.*\b(is|are|was|were)\b', 'Definition question'),
            (r'\b(?:why)\b', 'Reason question'),
            (r'\b(?:how)\b', 'Process question'),
            (r'\b(?:who)\b', 'Person question'),
            (r'\b(?:when)\b', 'Time question'),
            (r'\b(?:where)\b', 'Location question')
        ]

        for sentence in sentences[:10]:  # Limit to 10 sentences
            for pattern, q_type in patterns:
                if re.search(pattern, sentence.lower()):
                    # Create a cloze deletion question
                    words = sentence.split()
                    if len(words) > 5:
                        key_word = random.choice([w for w in words if len(w) > 4 and w.isalpha()])
                        question = sentence.replace(key_word, '_____')

                        flashcards.append({
                            'question': question,
                            'answer': key_word,
                            'difficulty': 'medium',
                            'type': q_type
                        })
                        break

        # If no pattern matches, create vocabulary questions
        if not flashcards and len(sentences) > 0:
            words = re.findall(r'\b[a-zA-Z]{5,}\b', text)
            word_freq = defaultdict(int)
            for word in words:
                word_freq[word.lower()] += 1

            common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

            for word, freq in common_words:
                flashcards.append({
                    'question': f"What does '{word}' mean in the context?",
                    'answer': word,
                    'difficulty': 'easy' if freq > 2 else 'medium',
                    'type': 'Vocabulary'
                })

        return flashcards[:5]  # Return max 5 flashcards

    except Exception as e:
        return [{
            'question': 'Error generating flashcards',
            'answer': 'Please try with different text',
            'difficulty': 'easy',
            'type': 'Error'
        }]


def update_difficulty(card, correct):
    """
    Simple difficulty tracking
    """
    if correct:
        if card['difficulty'] == 'hard':
            card['difficulty'] = 'medium'
        elif card['difficulty'] == 'medium':
            card['difficulty'] = 'easy'
    else:
        if card['difficulty'] == 'easy':
            card['difficulty'] = 'medium'
        elif card['difficulty'] == 'medium':
            card['difficulty'] = 'hard'
        
                      