import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
my_key = os.getenv('MY_KEY')
genai.configure(api_key=my_key)

st.title("Gemini-Bot : 상다미😊")

## 파라미터 바꿔보기
generation_config = genai.GenerationConfig(temperature=0.5, stop_sequences=["!"], max_output_tokens= 300)


safety_settings=[
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_LOW_AND_ABOVE", ## BLOCK_NONE, BLOCK_ONLY_HIGH, BLOCK_MEDIUM_AND_ABOVE, BLOCK_LOW_AND_ABOVE 등이 있다.
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_LOW_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_LOW_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_LOW_AND_ABOVE",
        },
    ]



@st.cache_resource
def load_model():
    model = genai.GenerativeModel('gemini-1.5-flash-latest', generation_config=generation_config, safety_settings=safety_settings)
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
