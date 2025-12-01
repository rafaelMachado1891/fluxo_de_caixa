WITH plano_contas AS (
    SELECT
        conta_contabil_credito,
        conta_contabil_debito,
        debito_codigo_conta,
        debito_descricao,
        credito_codigo_conta,
        credito_descricao
    FROM 
        {{ source('db', 'tbl_fluxo') }}
),
contas_tratadas AS (
    SELECT
        conta_contabil_credito:: INTEGER AS conta_contabil_credito,
        conta_contabil_debito:: INTEGER AS conta_contabil_debito,
        debito_codigo_conta:: TEXT AS debito_codigo_conta,
        credito_codigo_conta:: TEXT AS credito_codigo_conta,
        debito_descricao:: TEXT AS debito_descricao,
        credito_descricao:: TEXT AS credito_descricao
    FROM plano_contas
)

SELECT DISTINCT
    conta_contabil_credito,
    conta_contabil_debito,
    debito_codigo_conta,
    credito_codigo_conta,
    debito_descricao,
    credito_descricao
FROM contas_tratadas
