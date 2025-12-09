WITH titulos AS (
    SELECT
        *
    FROM 
        {{ source('fluxo_db', 'tbl_fluxo') }}
),
tbl_titulos_transformada AS (
    SELECT 
        numero_titulo:: TEXT AS numero_titulo,
        serie:: TEXT AS serie,
        data_emissao:: DATE AS data_emissao,
        vencimento:: DATE AS vencimento,
        data_pagamento:: DATE as data_pagamento,
        REPLACE(valor_titulo,',' , '.'):: DECIMAL AS valor_titulo,
        CASE WHEN
            tipo_credor = 2 OR tipo_credor = 3 THEN 'S'
            ELSE 'E' END:: text AS tipo_pagamento,
        instituicao:: INTEGER AS instituicao,
        situacao_titulo:: INTEGER AS situacao_titulo,
        codigo_credito:: INTEGER AS conta_contabil_credito,
        codigo_debito:: INTEGER AS conta_contabil_debito,
        id_cliente:: INTEGER AS id_cliente
    FROM titulos
)

SELECT 
    numero_titulo,
    serie,
    data_emissao,
    vencimento,
    CASE
        WHEN data_pagamento = '1753-01-01' THEN NULL
        ELSE data_pagamento
    END AS data_pagamento,
    valor_titulo,
    tipo_pagamento,
    CASE
        WHEN instituicao = '0' THEN 2
        ELSE instituicao
    END AS instituicao,
    situacao_titulo,
    COALESCE(conta_contabil_credito,0) AS conta_contabil_credito,
    COALESCE(conta_contabil_debito,0) AS conta_contabil_debito,
    id_cliente
FROM tbl_titulos_transformada