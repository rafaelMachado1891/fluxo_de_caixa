import streamlit as st
import requests

API_URL = "http://localhost:8000/perguntar"

st.title("Assistente de Fluxo de Caixa")

if "pergunta" not in st.session_state:
    st.session_state.pergunta = ""

def enviar():
    try:
        response = requests.post(
            API_URL,
            json={
                "pergunta": st.session_state.pergunta
            },
            timeout=30
        )

        data = response.json()
        st.session_state.resposta = data["resposta"]

    except Exception as e:
        st.session_state.resposta = "⚠️ Erro ao se comunicar com a API."

    st.session_state.pergunta = ""

st.text_input(
    "Pergunte algo sobre o fluxo de caixa",
    key="pergunta",
    on_change=enviar
)

if "resposta" in st.session_state:
    st.success(st.session_state.resposta)
