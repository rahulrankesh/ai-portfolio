import streamlit as st

# --- Basic page config ---
st.set_page_config(page_title="CG-ChitraGupt", page_icon="🤖", layout="centered")

# --- Custom CSS for styling ---
st.markdown(
    """
    <style>
    .chat-container {
        max-width: 600px;
        margin: auto;
        padding: 1rem;
    }
    .chat-bubble {
        border-radius: 15px;
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 1rem;
        line-height: 1.4;
    }
    .bot {
        background-color: #f1f1f1;
        text-align: left;
    }
    .user {
        background-color: #DCF8C6;
        text-align: right;
        margin-left: auto;
    }
    .avatar {
        display: flex;
        align-items: center;
        margin-bottom: 0.4rem;
    }
    .avatar img {
        border-radius: 50%;
        width: 32px;
        height: 32px;
        margin-right: 0.5rem;
    }
    .button-row {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 1rem;
    }
    .stButton > button {
        border-radius: 20px;
        background: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        border: none;
        cursor: pointer;
    }
    .stButton > button:hover {
        background: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session state for storing chat history ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history.append(
        {"role": "bot", "avatar": "😊", "content": "Hello! I’m **CG-ChitraGupt**, your guide. Ask me anything or pick a question below!"}
    )

# --- Function to render chat history ---
def render_chat():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"] == "bot":
            st.markdown(
                f"""
                <div class="avatar"><img src="https://i.ibb.co/SmilingAvatar.png" alt="bot"/> 
                <div class="chat-bubble bot">{msg["content"]}</div></div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-bubble user">{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

# --- Function to handle response logic ---
def get_bot_response(user_input):
    responses = {
        "Who are you?": "I am CG-ChitraGupt 🤖, a chatbot designed to assist you with queries.",
        "What can you do?": "I can answer pre-defined questions, show information, and guide you.",
        "Tell me a fun fact": "Did you know? The word *ChitraGupt* means 'hidden picture' in Sanskrit 📜.",
    }
    return responses.get(user_input, "I didn’t quite get that, but I’m learning every day!")

# --- Show chat ---
render_chat()

# --- Floating quick buttons ---
st.markdown('<div class="button-row">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("Who are you?"):
        st.session_state.chat_history.append({"role": "user", "content": "Who are you?"})
        st.session_state.chat_history.append({"role": "bot", "avatar": "😊", "content": get_bot_response("Who are you?")})
with col2:
    if st.button("What can you do?"):
        st.session_state.chat_history.append({"role": "user", "content": "What can you do?"})
        st.session_state.chat_history.append({"role": "bot", "avatar": "😊", "content": get_bot_response("What can you do?")})
with col3:
    if st.button("Tell me a fun fact"):
        st.session_state.chat_history.append({"role": "user", "content": "Tell me a fun fact"})
        st.session_state.chat_history.append({"role": "bot", "avatar": "😊", "content": get_bot_response("Tell me a fun fact")})
st.markdown('</div>', unsafe_allow_html=True)

# --- User free text input ---
user_input = st.text_input("Type your message:")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    bot_reply = get_bot_response(user_input)
    st.session_state.chat_history.append({"role": "bot", "avatar": "😊", "content": bot_reply})

# Refresh chat with new messages
render_chat()
