from backend.utils_db import Conexao_dw
from sqlalchemy import text



def executar_query(query: str, params: dict | None=None):
    conexao = Conexao_dw(conn_id="postgres_fluxo")
    engine = Conexao_dw.criar_engine()

    with engine.connect() as conn:
        resultado = conn.execute(text(query), params or {})
        return resultado.fetchone()