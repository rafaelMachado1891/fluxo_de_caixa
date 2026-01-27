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
    data = st.session_state.resposta

    if "texto" in data:
        st.markdown(data["texto"])

    if data.get("dados", {}).get("detalhes"):
        tabela = data["dados"]["detalhes"].get("por_semana")
        if tabela:
            df = pd.DataFrame(tabela)
            st.dataframe(df)