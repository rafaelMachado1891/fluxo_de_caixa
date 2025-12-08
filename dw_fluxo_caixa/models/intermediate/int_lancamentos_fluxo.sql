WITH int_lancamentos AS (
    SELECT
        numero_titulo,
        tipo_pagamento,
        data_recebimento,
        valor,
        conta_contabil_credito,
        conta_contabil_debito,
        id_cliente,
        instituicao
    FROM
        {{ ref('stg_lancamento_fluxo') }}
),

tabela_tratada AS (
    SELECT
        numero_titulo,
        CASE
            WHEN tipo_pagamento = 'D' THEN 'S'
            ELSE 'E'
        END AS tipo_pagamento,
        data_recebimento,
        valor,
        CASE
            WHEN conta_contabil_credito = 0 THEN conta_contabil_debito
            ELSE conta_contabil_credito
        END AS id_conta_contabil,
        id_cliente,
        instituicao
    FROM 
        int_lancamentos
)

SELECT * FROM tabela_tratada