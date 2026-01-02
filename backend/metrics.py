from datetime import date
from db import executar_query


def saldo_operacional_mes(ano: int, mes: int) -> float:
    ano_mes = f"{ano}-{mes:02d}"

    sql = """
        SELECT 
            SUM(valor_titulo) AS saldo
        FROM public_marts.marts_lancamentos
        WHERE tipo_fluxo = 'REALIZADO'
          AND ano_mes = :ano_mes

"""

    resultado = executar_query(
        sql,        
        {"ano_mes": ano_mes}
        
    )

    return resultado[0]