from datetime import date
from db import executar_query_all

def calcular_total_entradas_saidas_por_mes(
    ano: int | None = None,
    mes: int | None = None
):
    hoje = date.today()

    ano = ano if ano is not None else hoje.year
    mes = mes if mes is not None else hoje.month

    ano_mes = f"{ano}-{mes:02d}"

    query = """
        SELECT
            a.ano_mes,
            ROUND(SUM(CASE WHEN a.tipo_pagamento = 'E' THEN a.valor_titulo ELSE 0 END), 2) AS entradas,
            ROUND(SUM(CASE WHEN a.tipo_pagamento = 'S' THEN a.valor_titulo ELSE 0 END), 2) AS saidas,
            ROUND(
                SUM(CASE WHEN a.tipo_pagamento = 'E' THEN a.valor_titulo ELSE 0 END)
              - SUM(CASE WHEN a.tipo_pagamento = 'S' THEN a.valor_titulo ELSE 0 END), 2
            ) AS saldo_operacional
        FROM public_marts.marts_lancamentos a
        
        
        WHERE a.tipo_fluxo = 'PROJETADO'
          AND a.ano_mes = :ano_mes
        GROUP BY a.ano_mes
    """

    return executar_query_all(query, {"ano_mes": ano_mes})