WITH int_titulos AS (
    SELECT
        *
    FROM 
        {{ ref('stg_titulos') }}
),
tbl_titulos_transformada AS (
    SELECT 
        numero_titulo,
        data_emissao,
        vencimento,
        data_pagamento,
        valor_titulo,
        tipo_pagamento,
        instituicao,
        CASE situacao_titulo
            WHEN 1 THEN 'PENDENTE'
            WHEN 3 THEN 'PAGO'
            WHEN 4 THEN 'PARCIALMENTE_PAGO'
            WHEN 5 THEN 'CANCELADO'
            ELSE 'OUTRO'
        END:: TEXT AS situacao_titulo,
        CASE WHEN
            conta_contabil_credito = 0 THEN conta_contabil_debito
            ELSE conta_contabil_credito END:: INTEGER AS id_conta_contabil,
        id_cliente
    FROM int_titulos
)

SELECT 
    numero_titulo,
    data_emissao,
    vencimento,
    data_pagamento,
    valor_titulo,
    tipo_pagamento,
    instituicao,
    situacao_titulo,
    CASE WHEN 
        id_conta_contabil = 0 THEN 9999
        ELSE id_conta_contabil END AS id_conta_contabil,
    id_cliente
FROM tbl_titulos_transformada