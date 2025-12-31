import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.agent import responder

st.title("Assistente de Fluxo de Caixa")

pergunta = st.text_input("Pergunte algo sobre o fluxo de caixa")

if pergunta:
    resposta = responder(pergunta)
    st.success(resposta)