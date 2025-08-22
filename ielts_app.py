import streamlit as st 
import passage_utils as utils
import passage_summarizer as summarizer
import eng_flashcards as flashcards
import lang_feedback

st.set_page_config(page_title='IELTS Study Buddy', layout='wide')
st.title("📚 Study Assistant: IELTS Quiz & Flashcards")

# --- File Upload ---
uploaded_file = st.file_uploader('Upload your passage', type=['pdf', 'txt', 'docx'])

if uploaded_file is not None:
    # Extract text once and persist in session
    text = utils.extract_text(uploaded_file)
    st.session_state['passage_text'] = text
    
    st.write('### Extracted Passage')
    st.write(text)
    
    # --- Summarization ---
    @st.cache_data
    def get_summary(_text):
        return summarizer.summarize_text(_text)
    st.subheader('Summary')
    summary = get_summary(text)
    for s in summary:
        st.write("- " + s)
        
    # --- Flashcards / Quiz Generation ---
    @st.cache_data
    def get_flashcards(_text):
        return flashcards.generate_flashcards(_text)
    if 'flashcards' not in st.session_state:
        st.session_state.flashcards = get_flashcards(text)
    
    st.subheader("Flashcards")
    flashcards_list = st.session_state.flashcards
    
    if flashcards_list:
        for i, card in enumerate(flashcards_list):
            st.write(f"**Q{i+1}:** {card['question']}")
            user_ans = st.text_input(f"Your answer for Q{i+1}:", key=f"ans_{i}")
            if st.button(f"Submit Q{i+1}", key=f"btn_{i}"):
                correct = user_ans.strip().lower() == card["answer"].lower()
                flashcards.update_difficulty(card, correct)
                if correct:
                    st.success("Correct ✅")
                else:
                    st.error(f"Wrong ❌ | Correct answer: {card['answer']}")
                st.info(f"Difficulty: {card['difficulty']}")
    
    # --- Feedback ---
    st.subheader("Language Feedback")
    feedback_list = lang_feedback.generate_feedback(text, lang='en')  # Or 'both' if mixed lang
    
    if feedback_list:
        for f in feedback_list:
            st.write(f"**Sentence:** {f['sentence']}")
            st.write(f"**Issue:** {f['issue']}")
            st.write(f"**Tip:** {f['tip']}")
            st.write(f"**Tip (Arabic):** {f['translation_tip']}")
            st.write("---")
    else:
        st.write('No major issues! Keep going!')