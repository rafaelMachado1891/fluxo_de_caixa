WITH lancamentos AS (
    SELECT 
        "NumTitulo",
        "tipo",
        "DataReceb",
        "valor",
        "ContaContabil",
        "ContaContabilDebito",
        "Tipo_C",
        "Codigo_C",
        "Instituicao"
    FROM 
        {{ source('fluxo_db', 'tbl_lancamentos_fluxo') }}
),

tabela_tratada AS (
    SELECT
        "NumTitulo":: TEXT AS numero_titulo,
        "tipo":: TEXT AS tipo_pagamento,
        "DataReceb":: DATE AS data_recebimento,
        REPLACE("valor", ',', '.'):: DECIMAL AS valor,
        "ContaContabil":: INTEGER AS conta_contabil_credito,
        "ContaContabilDebito":: INTEGER AS conta_contabil_debito,
        "Tipo_C":: INTEGER AS tipo_pagameto,
        "Codigo_C":: INTEGER AS id_cliente,
        "Instituicao":: INTEGER AS instituicao
    FROM 
        lancamentos
)

SELECT * FROM tabela_tratada