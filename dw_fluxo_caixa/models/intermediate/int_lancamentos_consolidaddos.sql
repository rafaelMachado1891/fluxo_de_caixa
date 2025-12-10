WITH lancamentos AS (
    SELECT 
        a.*,
        b.numero_titulo AS titulo_vinculado
    FROM 
        {{ ref('int_lancamentos_fluxo') }} a 
    LEFT JOIN
        {{ ref('int_titulos') }} b 
    ON a.numero_titulo = b.numero_titulo AND
       a.numero_titulo <> '0' AND
       a.serie = b.serie AND
       a.id_cliente = b.id_cliente
    WHERE b.numero_titulo IS NULL

),

titulos AS (
    SELECT
        *,
        'TITULO_VINCULADO':: TEXT AS titulo_vinculado
    FROM 
        {{ ref('int_titulos') }}
),

consolidado AS (
    SELECT * FROM lancamentos
    UNION ALL
    SELECT * FROM titulos
)

SELECT * FROM consolidado

