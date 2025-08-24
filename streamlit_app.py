import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="CG-ChitraGupt", layout="wide")

st.markdown("<h2 style='text-align:center;'>Welcome to CG-ChitraGupt</h2>", unsafe_allow_html=True)

chatbot_html = """
<style>
/* Floating button */
#chat-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #4CAF50;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  font-size: 28px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.2);
  z-index: 9999;
}

/* Chat window */
#chat-window {
  position: fixed;
  bottom: 90px;
  right: 20px;
  width: 300px;
  max-height: 400px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  display: none;
  flex-direction: column;
  font-family: Arial, sans-serif;
  overflow: hidden;
}

/* Chat header */
#chat-header {
  background: #4CAF50;
  color: white;
  padding: 12px;
  font-size: 16px;
  font-weight: bold;
}

/* Chat body */
#chat-body {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  font-size: 14px;
}

/* Message bubbles */
.bot-msg, .user-msg {
  margin: 6px 0;
  padding: 8px 12px;
  border-radius: 14px;
  max-width: 80%;
  clear: both;
}

.bot-msg {
  background: #f1f1f1;
  float: left;
}

.user-msg {
  background: #4CAF50;
  color: white;
  float: right;
}

/* Buttons for predefined Qs */
.question-btns {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}

.question-btns button {
  flex: 1;
  background: #e8f5e9;
  border: 1px solid #4CAF50;
  border-radius: 10px;
  padding: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: transform 0.2s ease;
}

.question-btns button:hover {
  transform: scale(1.05);
  background: #c8e6c9;
}
</style>

<div id="chat-button">💬</div>

<div id="chat-window">
  <div id="chat-header">🤖 CG-ChitraGupt</div>
  <div id="chat-body">
    <div class="bot-msg">😊 Hello! I am CG-ChitraGupt. How can I guide you today?</div>
    <div class="question-btns">
      <button onclick="sendMessage('Who are you?')">Who are you?</button>
      <button onclick="sendMessage('Tell me about Karma')">Tell me about Karma</button>
      <button onclick="sendMessage('Give me guidance')">Give me guidance</button>
    </div>
  </div>
</div>

<script>
const chatButton = document.getElementById("chat-button");
const chatWindow = document.getElementById("chat-window");
const chatBody = document.getElementById("chat-body");

chatButton.addEventListener("click", () => {
  chatWindow.style.display = chatWindow.style.display === "flex" ? "none" : "flex";
});

function sendMessage(text) {
  // User message
  let userDiv = document.createElement("div");
  userDiv.className = "user-msg";
  userDiv.innerText = text;
  chatBody.appendChild(userDiv);

  // Bot reply after delay
  setTimeout(() => {
    let botDiv = document.createElement("div");
    botDiv.className = "bot-msg";

    if (text === "Who are you?") {
      botDiv.innerText = "I am CG-ChitraGupt, your guide tracking actions and giving wisdom!";
    } else if (text === "Tell me about Karma") {
      botDiv.innerText = "Karma is the law of cause and effect. Good deeds bring good results.";
    } else if (text === "Give me guidance") {
      botDiv.innerText = "Stay honest, stay kind, and remember: your actions write your destiny.";
    } else {
      botDiv.innerText = "I am still learning. Please choose one of the options.";
    }

    chatBody.appendChild(botDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
  }, 600);

  chatBody.scrollTop = chatBody.scrollHeight;
}
</script>
"""

components.html(chatbot_html, height=600)
