from datetime import date
from db import executar_query, executar_query_all


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


def top_5_contas_saidas(ano: int, mes: int) -> list[dict]:
    ano_mes = f"{ano}-{mes:02d}"

    sql = """
        SELECT
            b.conta_contabil,
            SUM(a.valor_titulo) AS valor_total
        FROM public_marts.marts_lancamentos a
        JOIN public_marts.dim_plano_contas b
            ON a.id_conta_contabil = b.codigo
        WHERE a.tipo_fluxo = 'REALIZADO'
          AND a.tipo_pagamento = 'S'
          AND a.ano_mes = :ano_mes
        GROUP BY b.conta_contabil
        ORDER BY valor_total 
        LIMIT 5
    """

    resultados = executar_query_all(
        sql, 
        {"ano_mes": ano_mes}
        )

    return resultados