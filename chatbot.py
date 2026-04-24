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
import pickle
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.title("💬 TF-IDF Chatbot (No Transformers, No FAISS)")

vectorizer, X, df = pickle.load(open("tfidf_model.pkl", "rb"))

def retrieve_answer(query):
    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, X).flatten()
    top_idx = scores.argmax()
    row = df.iloc[top_idx]
    return row["text"], row.get("image", None)

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Type your message:")

if st.button("Send"):
    if user_input.strip():
        st.session_state.messages.append(("You", user_input))

        answer, image = retrieve_answer(user_input)
        bot_msg = answer

        st.session_state.messages.append(("Bot", bot_msg, image))

# Display messages
for msg in st.session_state.messages:
    sender = msg[0]
    if sender == "You":
        st.markdown(f"**🧑‍💻 You:** {msg[1]}")
    else:
        text = msg[1]
        image = msg[2]
        st.markdown(f"**🤖 Bot:** {text}")
        if image:
            st.image(image)
