import streamlit as st
import json
import difflib

# --- Load FAQ from JSON file ---
with open("faq.json", "r") as f:
    faq_data = json.load(f)

# --- Helper: find closest FAQ answer ---
def get_best_answer(user_input, faq_data):
    questions = [item["question"] for item in faq_data]
    match = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.4)
    if match:
        for item in faq_data:
            if item["question"] == match[0]:
                return item["answer"]
    return "🤖 Sorry, I couldn’t find an exact answer. Please check the FAQ buttons!"

# --- Page config ---
st.set_page_config(page_title="CG Chatbot", page_icon="🤖", layout="centered")

# --- Title ---
st.title("🤖 CG Chatbot")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Floating Question Buttons ---
st.markdown("### Ask Me:")
cols = st.columns(len(faq_data))
for i, item in enumerate(faq_data):
    if cols[i].button(item["question"]):
        st.session_state.messages.append({"role": "user", "content": item["question"]})
        st.session_state.messages.append({"role": "assistant", "content": f"🤖 {item['answer']}"})
        st.rerun()

# --- User input ---
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    answer = get_best_answer(user_input, faq_data)
    st.session_state.messages.append({"role": "assistant", "content": f"🤖 {answer}"})
    st.rerun()
