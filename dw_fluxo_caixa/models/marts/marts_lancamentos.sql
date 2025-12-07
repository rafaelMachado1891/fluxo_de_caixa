WITH lancamentos AS (
    SELECT
        numero_titulo,
        data_emissao,
        vencimento,
        data_pagamento,
        vencimento - data_emissao AS prazo,
        valor_titulo,
        id_conta_contabil,
        tipo_pagamento,
        situacao_titulo,     
        instituicao,
        id_cliente,
        CASE 
            WHEN data_pagamento = NULL THEN 'PROJETADO'
            ELSE 'REALIZADO'
        END AS tipo_fluxo

    FROM 
        {{ ref('int_titulos') }}
)

SELECT * FROM lancamentos ORDER BY vencimento