# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



import streamlit as st
from utils_db import Conexao_dw
from sqlalchemy import text

st.title("Teste de conexão com o banco")

try:
    conexao = Conexao_dw()
    engine = conexao.criar_engine()

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).fetchone()

    st.success(f"Conexão OK ✅ Resultado: {result[0]}")

except Exception as e:
    st.error("Erro ao conectar no banco ❌")
    st.exception(e)

import streamlit as st
from agent import responder

st.title("Assistente de Fluxo de Caixa")

pergunta = st.text_input("Pergunte algo sobre o fluxo de caixa")

if pergunta:
    resposta = responder(pergunta)
    st.success(resposta)
