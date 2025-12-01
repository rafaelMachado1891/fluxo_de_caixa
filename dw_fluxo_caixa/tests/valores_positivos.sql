SELECT 
    valor_titulo
FROM {{ ref('stg_titulos') }}
WHERE valor_titulo < 0