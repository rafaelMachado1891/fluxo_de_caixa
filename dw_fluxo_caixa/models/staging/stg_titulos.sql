WITH titulos AS (
    SELECT
        *
    FROM 
        {{ source('db', 'tbl_fluxo') }}
),
tbl_titulos_transformada AS (
    SELECT 
        numero_titulo:: TEXT AS numero_titulo,
        TO_CHAR(data_emissao:: DATE, 'DD-MM-YYYY') AS data_emissao,
        TO_CHAR(vencimento:: DATE, 'DD-MM-YYYY') AS vencimento,
        CAST(REPLACE(valor_titulo,',' , '.')AS DECIMAL) AS valor_titulo
    FROM titulos
)

SELECT * FROM tbl_titulos_transformada