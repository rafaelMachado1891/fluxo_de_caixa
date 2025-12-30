from src.utils import ConexaoComBanco
from sqlalchemy import text



def executar_query(query: str, params: dict | None=None):
    conexao = ConexaoComBanco(conn_id="postgres_fluxo")
    engine = ConexaoComBanco.criar_engine()

    with engine.connect() as conn:
        resultado = conn.execute(text(query), params or {})
        return resultado.fetchone()