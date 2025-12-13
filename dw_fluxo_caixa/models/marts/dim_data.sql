WITH mart_dim_date AS (
SELECT
    date_day AS data,
    month_of_year AS mes,
    month_name_short AS nome_mes,
    quarter_of_year AS trimestre,
    year_number AS ano
FROM 
    {{ ref('int_dim_date') }}
)

SELECT * FROM mart_dim_date