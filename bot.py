import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
my_key = os.getenv('MY_KEY')
genai.configure(api_key=my_key)

st.title("Gemini-student-counsel-Bot : 상다미")

@st.cache_resource
def load_model():
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    print("model loaded...")
    return model

model = load_model()

if "chat_session" not in st.session_state:
    st.session_state["chat_session"] = model.start_chat(history=[])

for content in st.session_state.chat_session.history:
    with st.chat_message("상다미" if content.role == "model" else "user"):
        st.markdown(content.parts[0].text)

if prompt := st.chat_input("무엇이든 제게 편하게 상담해주세요!"):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
