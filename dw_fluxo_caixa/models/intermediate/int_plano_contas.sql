WITH plano_contas AS (
    SELECT
        codigo,
        codigo_conta_contabil,
        conta_contabil,
        data_inclusao
    FROM 
        {{ ref('stg_plano_contas') }}
),

plano_contas_tratado AS (
    INSERT INTO plano_contas
)

SELECT * FROM plano_contas
