import streamlit as st

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

    # Dummy bot reply (for now, just echoes)
    response = f"Echo: {prompt}"
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
