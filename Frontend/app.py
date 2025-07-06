import streamlit as st
import requests

st.title("📅 Calendar Chatbot")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.chat_input("Say something...")

if user_input:
    st.session_state.chat.append(("user", user_input))
    res = requests.post("https://calenderai-production.up.railway.app/chat", json={"text": user_input})
    print("STATUS:", res.status_code)
    print("TEXT:", res.text)
    bot_reply = res.json()["response"]
    st.session_state.chat.append(("bot", bot_reply))

for sender, msg in st.session_state.chat:
    st.chat_message(sender).write(msg)
