WITH lancamentos AS (
    SELECT
        SUM(valor_titulo) AS total_lancamento,
        id_conta_contabil,
        tipo_pagamento

    FROM 
        {{ ref('int_titulos')}}
    GROUP BY id_conta_contabil,
             tipo_pagamento

),

plano_conta AS (
    SELECT
        *
    FROM 
        {{ ref('int_plano_contas') }}
),

tabelas_agrupadas AS (
    SELECT
        a.tipo_pagamento,
        a.id_conta_contabil,
        a.total_lancamento,
        b.codigo_conta_contabil,
        b.conta_contabil
    FROM lancamentos a
    LEFT JOIN plano_conta b 
    ON a.id_conta_contabil = b.codigo

)

SELECT * FROM tabelas_agrupadas