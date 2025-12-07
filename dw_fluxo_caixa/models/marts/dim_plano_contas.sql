WITH plano_contas AS (
SELECT
    codigo,
    codigo_conta_contabil,
    conta_contabil
FROM 
    {{ ref('int_plano_contas') }}
)

SELECT * FROM plano_contas