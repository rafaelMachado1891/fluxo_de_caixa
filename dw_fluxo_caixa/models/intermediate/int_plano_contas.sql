WITH plano_contas AS (
    SELECT
        conta_contabil_credito,
        conta_contabil_debito,
        debito_codigo_conta,
        debito_descricao,
        credito_codigo_conta,
        credito_descricao
    FROM 
        {{ ref('stg_plano_contas') }}
),
contas_tratadas AS (
    SELECT
        CASE WHEN 
            conta_contabil_credito = 0 THEN conta_contabil_debito
            ELSE conta_contabil_credito END AS id_conta_contabil,
        CASE WHEN 
            debito_codigo_conta ISNULL THEN credito_codigo_conta
            ELSE debito_codigo_conta END AS conta_contabil,
        CASE WHEN 
            debito_descricao ISNULL THEN credito_descricao
            ELSE debito_descricao END AS descricao_conta_contabil
    FROM plano_contas
)

SELECT
    CASE WHEN 
        id_conta_contabil = 0 THEN 9999
        ELSE id_conta_contabil END AS id_conta_contabil,
    CASE WHEN 
        conta_contabil ISNULL THEN '9999'
        ELSE conta_contabil END AS conta_contabil,
    CASE WHEN
        descricao_conta_contabil ISNULL THEN 'NAO_INFORMADO'
        ELSE descricao_conta_contabil END AS descricao_conta_contabil
FROM contas_tratadas
