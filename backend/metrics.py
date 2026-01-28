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
                AND a.ano_mes = :ano_mes
            ),

            saldo_operacional AS (
                SELECT                 
                    SUM(valor_titulo) AS saldo_operacional                                    
                FROM 
                    public_marts.marts_lancamentos
                WHERE tipo_fluxo = 'REALIZADO' 
                AND 
                    data_pagamento <  CURRENT_DATE     
            ),

            saldo_inicial AS (
                SELECT 
                    saldo AS saldo_inicial	
                FROM public_marts.dim_saldo_inicial
            ),

            agregado AS (

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


def calcular_cobertura_de_caixa () -> int | None:
      
    return executar_query_scalar(    
        
        sql = """
                WITH saldo_operacional_projetado AS (
            SELECT 
                ano_mes, 
                SUM(valor_titulo) AS total_titulo
            FROM 
                public_marts.marts_lancamentos 
            WHERE 
                tipo_fluxo = 'PROJETADO' AND 
                tipo_pagamento = 'S' 
            GROUP BY 
                ano_mes
        ),

        media_saldo_projetado AS (
            SELECT 
                AVG(total_titulo) AS saldo_operacional_medio_projetado
            FROM 
                saldo_operacional_projetado 
            
        ),
        saldo_operacional_realizado AS (
            SELECT
                SUM(valor_titulo) AS saldo_operacional_realizado
            FROM
                public_marts.marts_lancamentos 
            WHERE 
                tipo_fluxo = 'REALIZADO' 
        )
        SELECT 
            ROUND((saldo_operacional_realizado + saldo) / ABS(saldo_operacional_medio_projetado),0) AS cobertura_de_caixa
            
        FROM 
            media_saldo_projetado 
        CROSS JOIN 
            saldo_operacional_realizado
        CROSS JOIN 
            public_marts.dim_saldo_inicial
        
        
        """
    )


def calcular_variacoes_saidas_entradas_saldo_operacional(
        ano: int | None = None, 
        mes: int | None = None
) -> list[dict]:

    hoje = date.today()

    ano = ano if ano is not None else hoje.year
    mes = mes if mes is not None else hoje.month

    ano_mes = f"{ano}-{mes:02d}"

    query = """
        WITH lancamentos AS (
        SELECT
            ano_mes,
            SUM(valor_titulo) FILTER (WHERE tipo_pagamento = 'E') AS entradas,
            SUM(valor_titulo) FILTER (WHERE tipo_pagamento = 'S') AS saidas,
            SUM(valor_titulo) FILTER (WHERE tipo_pagamento = 'E') + 
            SUM(valor_titulo) FILTER (WHERE tipo_pagamento = 'S') AS saldo_operacional
        FROM public_marts.marts_lancamentos a
        LEFT JOIN public_intermediate.int_dim_date b
        ON a.vencimento = b.date_day
        GROUP BY 
            ano_mes
        ORDER BY 
            ano_mes
        ),

        variacoes AS (
            SELECT
                ano_mes,
                entradas,
                LAG(entradas) OVER(ORDER BY ano_mes) AS entradas_mes_anterior,
                ROUND(entradas / LAG(entradas) OVER(ORDER BY ano_mes) -1,2)AS variacoes_entradas,
                saidas,
                LAG(saidas) OVER(ORDER BY ano_mes) AS saidas_mes_anterior,
                ROUND(saidas / LAG(saidas) OVER(ORDER BY ano_mes) -1,2)AS variacoes_saidas,
                saldo_operacional,
                LAG(saldo_operacional) OVER(ORDER BY ano_mes) AS saldo_operacional_mes_anterior,
                ROUND(saldo_operacional / LAG(saldo_operacional) OVER(ORDER BY ano_mes) -1,2) AS variacao_saldo_operacional                    
            FROM 
                lancamentos
                )

        select * from variacoes WHERE ano_mes = :ano_mes
                
"""
     
    return executar_query_all(query, {"ano_mes": ano_mes})
        


