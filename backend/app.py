import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/perguntar"

st.title("Assistente de Fluxo de Caixa")

if "resposta" not in st.session_state:
    st.session_state.resposta = None

def enviar():
    try:
        response = requests.post(
            API_URL,
            json={
                "pergunta": st.session_state.pergunta,
                "contexto": {"dominio": "financeiro"}
            },
            timeout=30
        )

        data = response.json()
        st.session_state.resposta = data

    except Exception as e:
        st.session_state.resposta = {"erro": str(e)}

    st.session_state.pergunta = ""

st.text_input(
    "Pergunte algo sobre o fluxo de caixa",
    key="pergunta",
    on_change=enviar
)

if st.session_state.resposta:
    resp = st.session_state.resposta

    if not resp["success"]:
        st.error(resp["message"])
    else:
        st.markdown(resp["message"])

        detalhes = resp["data"].get("detalhes")
        if detalhes and "por_semana" in detalhes:
            df = pd.DataFrame(detalhes["por_semana"])
            st.dataframe(df)