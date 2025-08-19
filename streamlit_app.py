import streamlit as st

st.set_page_config(page_title="Karn AI • Portfolio", layout="centered")

st.title("👋 Hi, I'm Karn")
st.subheader("AI Enthusiast | Research & Invent | Future Leader")

st.write("""
Welcome to my portfolio!  
This website is built with **Streamlit** and showcases my work in **AI, projects, and research**.
""")

st.markdown("---")

st.header("🚀 Projects")
st.write("- Project 1: AI Chatbot")
st.write("- Project 2: Data Analytics Dashboard")
st.write("- Project 3: Vedic Tech Research")
st.markdown("---")
st.header("🤖 Chat with my AI")

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state["messages"]:
    st.write(msg)

# Input box
user_input = st.text_input("Type your question here...")

if user_input:
    # For now, just echo back — later we’ll connect it to AI
    response = f"You said: {user_input}"
    st.session_state["messages"].append(f"👤: {user_input}")
    st.session_state["messages"].append(f"🤖: {response}")
    st.experimental_rerun()
st.markdown("---")

st.header("📫 Connect with me")
st.write("[LinkedIn](https://linkedin.com) | [GitHub](https://github.com) | [Email](mailto:youremail@example.com)")
