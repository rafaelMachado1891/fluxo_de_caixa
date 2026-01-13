from utils_db import Conexao_dw
from sqlalchemy import text



def executar_query(query: str, params: dict | None=None):
    conexao = Conexao_dw()
    engine = conexao.criar_engine()

    with engine.connect() as conn:
        resultado = conn.execute(text(query), params or {})
        return resultado.fetchone()
    
def executar_query_all(sql: str, params: dict = None):
    engine = Conexao_dw().criar_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return [dict(row._mapping) for row in result.fetchall()]
    
def executar_query_scalar(sql: str, params: dict | None = None) -> float | None:
    engine = Conexao_dw().criar_engine()

    with engine.connect() as conn:
        row = conn.execute(text(sql), params or {}).fetchone()

        if row is None:
            return None

        valor = row[0]

        if valor is None:
            return None

        return float(valor)