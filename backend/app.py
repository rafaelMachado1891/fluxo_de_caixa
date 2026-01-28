import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/perguntar"

st.title("Assistente de Fluxo de Caixa")

if "resposta" not in st.session_state:
    st.session_state.resposta = {}

def enviar():
    try:
        response = requests.post(
            API_URL,
            json={
                "pergunta": st.session_state.pergunta,
                "contexto": st.session_state.get("contexto", {})
            },
            timeout=30
        )

        st.session_state.resposta = response.json()

    except Exception as e:
        st.session_state.resposta = {
            "success": False,
            "message": str(e),
            "data": {}
        }

    st.session_state.pergunta = ""


st.text_input(
    "Pergunte algo sobre o fluxo de caixa",
    key="pergunta",
    on_change=enviar
)

# ============================
# 🔥 PROTEÇÃO DEFINITIVA
# ============================
data = st.session_state.resposta or {}

# ============================
# RESPOSTA PRINCIPAL
# ============================
if isinstance(data, dict) and data.get("message"):
    st.markdown(data["message"])

# ============================
# DETALHES
# ============================
detalhes = (
    data.get("data", {}).get("detalhes")
    if isinstance(data.get("data"), dict)
    else None
)

if detalhes:
    st.subheader("📊 Detalhes")
    st.dataframe(pd.DataFrame([detalhes]))