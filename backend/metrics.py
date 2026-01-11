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

def entradas_saidas_projetadas (ano: int, mes: int) -> list[dict]:
    ano_mes = f"{ano}-{mes:02d}"

    query = """
        SELECT 
            ano_mes,
            week_of_year,
            tipo_pagamento,
            SUM(a.valor_titulo) AS valor
        FROM public_marts.marts_lancamentos a 
        JOIN public_intermediate.int_dim_date b
        ON a.vencimento = b.date_day
        WHERE tipo_fluxo = 'PROJETADO' AND a.ano_mes = :ano_mes
        GROUP BY ano_mes, week_of_year, tipo_pagamento
        ORDER BY 1, 2 
    """

    resultados = executar_query_all(
        query, 
        {"ano_mes": ano_mes}
        )

    return resultados

def saldo_operacional_projetado_negativo (ano: int, mes: int) -> list[dict]:
    ano_mes = f"{ano}-{mes:02d}"

    query = """
    WITH saldo_operacional_semanal AS (
        SELECT
            a.ano_mes,
            b.week_of_year,
            SUM(a.valor_titulo) AS saldo_operacional
        FROM public_marts.marts_lancamentos a
        JOIN public_intermediate.int_dim_date b
            ON a.vencimento = b.date_day
        WHERE a.tipo_fluxo = 'PROJETADO'
        AND a.ano_mes = :ano_mes
        GROUP BY
            a.ano_mes,
            b.week_of_year
    )

        SELECT
            ano_mes,
            week_of_year,
            saldo_operacional
        FROM saldo_operacional_semanal
        WHERE saldo_operacional < 0
        ORDER BY week_of_year ASC
    """

    resultados = executar_query_all(
        query, 
        {"ano_mes": ano_mes}
        )

    return resultados