from datetime import date
from db import executar_query_all, executar_query, executar_query_scalar

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
            b.week_of_year AS semana_ano,
            ROUND(SUM(CASE WHEN a.tipo_pagamento = 'E' THEN a.valor_titulo ELSE 0 END), 2) AS entradas,
            ROUND(SUM(CASE WHEN a.tipo_pagamento = 'S' THEN a.valor_titulo ELSE 0 END), 2) AS saidas,
            ROUND(
                SUM(CASE WHEN a.tipo_pagamento = 'E' THEN a.valor_titulo ELSE 0 END)
              + SUM(CASE WHEN a.tipo_pagamento = 'S' THEN a.valor_titulo ELSE 0 END), 2
            ) AS saldo_operacional
        FROM public_marts.marts_lancamentos a
        LEFT JOIN public_intermediate.int_dim_date b
        ON a.vencimento = b.date_day        
        WHERE a.tipo_fluxo = 'PROJETADO'
          AND a.ano_mes = :ano_mes
        GROUP BY a.ano_mes, b.week_of_year
        
    """

    return executar_query_all(query, {"ano_mes": ano_mes})


def calcular_saldo_operacional_projetado(ano: int | None = None, mes: int | None = None) -> float | None:
    
    hoje = date.today()

    ano = ano if ano is not None else hoje.year
    mes = mes if mes is not None else hoje.month
    
    ano_mes = f"{ano}-{mes:02d}"
    
    sql = """
        SELECT
            ROUND(
                SUM(CASE WHEN tipo_pagamento = 'E' THEN valor_titulo ELSE 0 END)
              + SUM(CASE WHEN tipo_pagamento = 'S' THEN valor_titulo ELSE 0 END), 2
            ) AS saldo_operacional
        FROM public_marts.marts_lancamentos
        WHERE tipo_fluxo = 'PROJETADO'
          AND ano_mes = :ano_mes
    """
    
    resultado = executar_query_scalar(sql,{"ano_mes": ano_mes})
    
    if resultado is None:
        return None

    return (resultado)

    
    print(type(resultado))
    

def calcular_saldo_final_projetado(ano: int | None = None, mes: int | None = None) -> float | None:
    
    hoje = date.today()

    ano = ano if ano is not None else hoje.year
    mes = mes if mes is not None else hoje.month
    
    ano_mes = f"{ano}-{mes:02d}"
    
    sql = """
            WITH saldo_projetado AS (

                SELECT
                    ROUND(
                        SUM(CASE WHEN a.tipo_pagamento = 'E' THEN a.valor_titulo ELSE 0 END)
                    +  SUM(CASE WHEN a.tipo_pagamento = 'S' THEN a.valor_titulo ELSE 0 END), 2
                    ) AS saldo_operacional_projetado
                FROM public_marts.marts_lancamentos a
                LEFT JOIN public_intermediate.int_dim_date b
                ON a.vencimento = b.date_day
                WHERE a.tipo_fluxo = 'PROJETADO'
                AND a.ano_mes = '2026-01'
            ),

            saldo_operacional AS (
                SELECT                 
                    SUM(valor_titulo) AS saldo_operacional                                    
                FROM 
                    public_marts.marts_lancamentos
                WHERE tipo_fluxo = 'REALIZADO' 
                AND 
                    vencimento <  CURRENT_DATE     
            ),

            saldo_inicial AS (
                SELECT 
                    saldo AS saldo_inicial	
                FROM public_marts.dim_saldo_inicial
            ),

           gregado AS (

                SELECT 
                *                
                FROM 
                    saldo_operacional
                CROSS JOIN 
                    saldo_inicial
                CROSS JOIN 
                    saldo_projetado
            )

                SELECT 
                    saldo_operacional + saldo_inicial + saldo_operacional_projetado AS 
                    saldo_final_projetado
                FROM 
                    agregado

            """
    
    resultado = executar_query_scalar(sql,{"ano_mes": ano_mes})
    
    if resultado is None:
        return None

    return (resultado)