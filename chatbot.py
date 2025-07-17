import streamlit as st
import requests
from PIL import Image

logo = Image.open("docs/upv_logo.png")
st.image(logo, width=200) 
st.set_page_config(page_icon="💬")
st.title("💬 Chatbot Financiero (RAG)")

API_URL = "http://localhost:8000/rag"  

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Formulario de entrada del usuario
if prompt := st.chat_input("Escribe tu pregunta sobre los documentos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Spinner mientras se consulta el RAG
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = requests.post(API_URL, json={"question": prompt})
                response.raise_for_status()
                answer = response.json()["answer"]
            except Exception as e:
                answer = f"❌ Error: {e}"

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


# streamlit run chatbot.py