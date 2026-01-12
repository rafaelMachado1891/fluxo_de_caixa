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

def alerta_contas_criticas () -> list[dict]:

    query = """
        WITH valor_total_saidas AS (
            SELECT
                a.ano_mes,
                c.codigo,
                c.conta_contabil,
                --b.week_of_year,
                ROUND(SUM(a.valor_titulo),2) AS total_saidas
            FROM public_marts.marts_lancamentos a
            JOIN public_intermediate.int_dim_date b
                ON a.vencimento = b.date_day
            LEFT JOIN public_marts.dim_plano_contas c
                ON a.id_conta_contabil = c.codigo
            WHERE a.tipo_fluxo = 'REALIZADO' AND
                a.tipo_pagamento = 'S'
            GROUP BY
            a.ano_mes, c.codigo, c.conta_contabil
            ORDER BY 2,1
        ),

        valor_medio AS (
            SELECT 
                ano_mes,
                codigo,
                conta_contabil,
                total_saidas,
                ROUND( AVG(total_saidas) OVER ( PARTITION BY codigo ORDER BY codigo, ano_mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW ), 2 ) AS media_movel_3m,
                ROW_NUMBER() OVER ( PARTITION BY codigo ORDER BY ano_mes DESC ) AS rn
                FROM valor_total_saidas 
                ORDER BY 2,1
        ),

        ultimo_valor_medio AS (
            SELECT 
                *
            FROM valor_medio
            WHERE rn = 1 
        ),

        fluxo_caixa_projetado AS (
            SELECT
                a.ano_mes,
                id_conta_contabil,
                ROUND(SUM(a.valor_titulo),2) AS total_saidas
            FROM public_marts.marts_lancamentos a
            JOIN public_intermediate.int_dim_date b
                ON a.vencimento = b.date_day  
            WHERE a.tipo_fluxo = 'PROJETADO' AND
                a.tipo_pagamento = 'S'
            GROUP BY
            a.ano_mes, id_conta_contabil
        ),

        agregado AS (
            SELECT 
                a.*,
                b.conta_contabil,
                b.media_movel_3m
            FROM fluxo_caixa_projetado a
            LEFT JOIN ultimo_valor_medio  b
            ON a.id_conta_contabil = b.codigo
        )

        SELECT 
            ano_mes,
            conta_contabil,
            total_saidas,
            media_movel_3m AS media_movel_3_meses
        FROM agregado WHERE total_saidas < media_movel_3m ORDER BY 1, 2
    """
    resultado = executar_query_all(query)
    return resultado

def calcular_total_saida_entradas_por_semana(
    ano: int = None,
    mes: int = None,
    semana: int = None
):
    hoje = date.today()
    ano = ano or hoje.year
    mes = mes or hoje.month
    semana = int(date.today().strftime("%U"))

    ano_mes = f"{ano}-{mes:02d}"

    query = """
        SELECT
            a.ano_mes,
            b.week_of_year AS semana_ano,
            ROUND(SUM(CASE WHEN a.tipo_pagamento = 'E' THEN a.valor_titulo ELSE 0 END), 2) AS entradas,
            ROUND(SUM(CASE WHEN a.tipo_pagamento = 'S' THEN a.valor_titulo ELSE 0 END), 2) AS saidas,
            ROUND(
                SUM(CASE WHEN a.tipo_pagamento = 'E' THEN a.valor_titulo ELSE 0 END)
              - SUM(CASE WHEN a.tipo_pagamento = 'S' THEN a.valor_titulo ELSE 0 END), 2
            ) AS saldo_operacional
        FROM public_marts.marts_lancamentos a
        JOIN public_intermediate.int_dim_date b
          ON a.vencimento = b.date_day
        WHERE a.tipo_fluxo = 'PROJETADO'
          AND a.ano_mes = :ano_mes
          AND b.week_of_year = :semana
        GROUP BY a.ano_mes, b.week_of_year
    """

    return executar_query_all(
        query,
        {
            "ano_mes": ano_mes,
            "semana": semana
        }
    )
