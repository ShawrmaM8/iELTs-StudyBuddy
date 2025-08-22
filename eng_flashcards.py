# Purpose: Generate flashcards from extracted text using spaCy-named entities

import spacy
nlp = spacy.load('en_core_web_sm')  # Load here for consistency

def generate_flashcards(text):
    """Return list of flashcards: {question, answer, difficulty}"""
    doc = nlp(text)
    flashcards = []
    
    for sent in doc.sents:
        for ent in sent.ents:  # Fixed: per sentence, not doc.ents
            q_text = sent.text.replace(ent.text, '______')
            flashcards.append({
                'question': q_text,
                'answer': ent.text,
                'difficulty': 'medium',
                'stats': {'attempts': 0, 'correct': 0}
            })
    return flashcards  # Moved outside loop
            
def update_difficulty(card, correct):
    card['stats']['attempts'] += 1  # Fixed: card, not cards
    if correct:
        card['stats']['correct'] += 1
    rate = card['stats']['correct'] / card['stats']['attempts']
    if rate >= 0.8:
        card['difficulty'] = 'easy'
    elif rate < 0.4:
        card['difficulty'] = 'hard'
    else:
        card['difficulty'] = 'medium'
        
        
                      