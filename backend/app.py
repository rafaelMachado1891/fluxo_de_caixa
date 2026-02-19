import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/perguntar"

st.set_page_config(page_title="Fluxo de Caixa", layout="wide")
st.title("📊 Assistente de Fluxo de Caixa")

# ============================
# ESTADO
# ============================
if "resposta" not in st.session_state:
    st.session_state.resposta = {}

if "contexto" not in st.session_state:
    st.session_state.contexto = {}

# ============================
# FUNÇÃO DE ENVIO
# ============================
def enviar():
    try:
        response = requests.post(
            API_URL,
            json={
                "pergunta": st.session_state.pergunta,
                "contexto": st.session_state.contexto
            },
            timeout=30
        )

        st.session_state.resposta = response.json()

    except Exception as e:
        st.session_state.resposta = {
            "success": False,
            "message": str(e),
            "data": None
        }

    st.session_state.pergunta = ""


# ============================
# INPUT
# ============================
st.text_input(
    "Pergunte algo sobre o fluxo de caixa:",
    key="pergunta",
    on_change=enviar
)

# ============================
# RESPOSTA
# ============================
data = st.session_state.resposta or {}

# ---------- TEXTO ----------
if isinstance(data, dict) and data.get("message"):
    st.markdown(data["message"])

# ---------- VISUALIZAÇÃO ----------
data_api = data.get("data")

if isinstance(data_api, dict):
    resultado = data_api.get("resultado", {})
    visualizacao = data_api.get("visualizacao")
else:
    resultado = {}
    visualizacao = None

# ---------- TABELA ----------
if visualizacao == "tabela":
    detalhes = resultado.get("detalhes", {})
    tabela = detalhes.get("tabela")

    if tabela:
        st.subheader("📋 Detalhamento")
        st.dataframe(pd.DataFrame(tabela), use_container_width=True, hide_index=True)

# ---------- DEBUG (opcional) ----------
with st.expander("🔍 Debug (dados brutos)"):
    st.json(data)