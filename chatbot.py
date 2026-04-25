# import streamlit as st

# st.set_page_config(page_title="Chatbot", page_icon="💬")

# st.title("💬 Simple Chatbot in Streamlit")

# if "messages" not in st.session_state:
#     st.session_state.messages = []


# def bot_response(user_input):
#     user_input = user_input.lower()

#     if "hello" in user_input or "hi" in user_input:
#         return "Hello! How can I help you today?"
#     elif "your name" in user_input:
#         return "I'm your Streamlit chatbot 🤖"
#     elif "bye" in user_input:
#         return "Goodbye! Have a great day!"
#     else:
#         return "I'm not sure how to answer that, but I'm learning 🙂"

# user_input = st.text_input("Type your message:")

# if st.button("Send"):
#     if user_input.strip() != "":
#         st.session_state.messages.append(("You", user_input))

#         reply = bot_response(user_input)
#         st.session_state.messages.append(("Bot", reply))

# for sender, message in st.session_state.messages:
#     if sender == "You":
#         st.markdown(f"**🧑‍💻 You:** {message}")
#     else:
#         st.markdown(f"**🤖 Bot:** {message}")

# app.py
import streamlit as st
import time
import os
import speech_recognition as sr
from groq import Groq

st.set_page_config(page_title="Groq AI Chatbot", page_icon="🤖")

st.title("🤖 Groq AI Chatbot")
st.caption("Fast • Free • AI powered 🚀")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ Groq API key not found! Restart terminal.")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []


def type_text(text, placeholder):
    typed = ""
    for char in text:
        typed += char
        placeholder.markdown(typed)
        time.sleep(0.01)

def get_voice():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening...")
            audio = r.listen(source)
        return r.recognize_google(audio)
    except:
        return None

def ai_response(user_input):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ FIXED MODEL
            messages=[
                {"role": "system", "content": "You are a helpful and friendly chatbot."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

col1, col2 = st.columns([4,1])

with col2:
    if st.button("🎤 Speak"):
        voice = get_voice()
        if voice:
            st.session_state.messages.append(("You", voice))

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append(("You", user_input))


for sender, msg in st.session_state.messages:
    if sender == "You":
        st.chat_message("user").write(msg)
    else:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            type_text(msg, placeholder)


if st.session_state.messages:
    last_sender, last_msg = st.session_state.messages[-1]

    if last_sender == "You":
        reply = ai_response(last_msg)
        st.session_state.messages.append(("Bot", reply))

        with st.chat_message("assistant"):
            placeholder = st.empty()
            type_text(reply, placeholder)
