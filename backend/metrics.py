from datetime import date
from backend.db import executar_query


def saldo_operacional_mes_atual():
    hoje = date.today()

    query = """
        SELECT COALESCE(SUM(valor_fluxo), 0) AS saldo
        FROM .public_marts.marts_lancamentos
        WHERE tipo_fluxo = 'REALIZADO'
          AND EXTRACT(YEAR FROM data_pagamento) = :ano
          AND EXTRACT(MONTH FROM data_pagamento) = :mes

"""

    resultado = executar_query(
        query,
        {
        "ano": hoje.year,
        "mes": hoje.month
        }
    )

    return resultado