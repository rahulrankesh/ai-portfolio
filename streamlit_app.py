import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page setup
st.set_page_config(page_title="Karn AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Karn AI Chatbot")
st.write("Ask me anything!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Query OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",   # you can also use "gpt-4o" or "gpt-3.5-turbo"
        messages=st.session_state["messages"]
    )

    reply = response.choices[0].message.content

    # Add assistant reply
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
