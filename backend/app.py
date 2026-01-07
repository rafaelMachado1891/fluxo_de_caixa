import streamlit as st
from agent import responder

st.title("Assistente de Fluxo de Caixa")

# Estado da pergunta
if "pergunta" not in st.session_state:
    st.session_state.pergunta = ""

# Estado de contexto (memória)
if "contexto" not in st.session_state:
    st.session_state.contexto = {
        "ano": None,
        "mes": None
    }

def enviar():
    try:
        resposta, novo_contexto = responder(
            st.session_state.pergunta,
            contexto=st.session_state.contexto
        )
        st.session_state.contexto.update(novo_contexto)
        st.session_state.resposta = resposta
    except Exception as e:
        st.session_state.resposta = f"⚠️ {str(e)}"

    # limpa a caixa de texto
    st.session_state.pergunta = ""

st.text_input(
    "Pergunte algo sobre o fluxo de caixa",
    key="pergunta",
    on_change=enviar
)

if "resposta" in st.session_state:
    st.success(st.session_state.resposta)