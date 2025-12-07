WITH plano_contas AS (
    SELECT
        codigo,
        codigo_conta_contabil,
        conta_contabil,
        data_inclusao
    FROM 
        {{ ref('stg_plano_contas') }}
),

contas_tratadas AS (
SELECT 
    *
FROM plano_contas

UNION ALL 

SELECT
    9999 AS codigo,
    '9999.1' AS codigo_conta_contabil,
    'NAO_INFORMADO' AS conta_contabil,
    CURRENT_DATE AS data_inclusao
)

SELECT * FROM contas_tratadas