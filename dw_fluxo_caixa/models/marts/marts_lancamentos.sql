WITH lancamentos AS (
    SELECT
        numero_titulo,
        data_emissao,
        vencimento,
        data_pagamento,
        vencimento - data_emissao AS prazo,
        CASE
            WHEN tipo_pagamento = 'S' 
                THEN valor_titulo * (-1)
            ELSE valor_titulo END AS valor_titulo, 
        id_conta_contabil,
        tipo_pagamento,
        situacao_titulo,     
        instituicao,
        id_cliente,
        tipo_fluxo

    FROM 
        {{ ref('int_lancamentos_consolidados') }}
)

SELECT * FROM lancamentos ORDER BY vencimento