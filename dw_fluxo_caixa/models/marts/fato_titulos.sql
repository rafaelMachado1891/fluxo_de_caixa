WITH mart_titulos AS (
SELECT
    valor_titulo,
    tipo_pagamento,
    situacao_titulo,
    vencimento
FROM 
    {{ ref('int_titulos') }}
),

dim_date AS (
    SELECT
        date_day AS data,
        month_name AS nome_do_mes,
        year_number AS ano,
        month_of_year AS mes
    FROM 
        {{ ref('int_dim_date') }}
)
SELECT 
    a.tipo_pagamento,
    SUM(a.valor_titulo),
    b.nome_do_mes,
    b.mes,
    b.ano
FROM mart_titulos a
JOIN dim_date b 
ON a.vencimento = b.data
WHERE a.situacao_titulo = 1
GROUP BY b.nome_do_mes, a.tipo_pagamento, b.mes, b.ano