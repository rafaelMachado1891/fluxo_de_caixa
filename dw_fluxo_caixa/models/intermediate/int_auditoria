SELECT 
    b.*,
    a.numero_titulo AS titulo_encontrado,
    a.data_pagamento AS data_pagamento_titulo,
    CASE 
        WHEN a.numero_titulo IS NULL THEN 'LANÇAMENTO_MANUAL'
        ELSE 'LANÇAMENTO_VINCULADO_TITULO'
    END AS tipo_origem_fluxo
FROM public_intermediate.int_lancamentos_fluxo b
LEFT JOIN public_intermediate.int_titulos a
    ON a.numero_titulo = b.numero_titulo 
    AND a.data_pagamento BETWEEN b.data_recebimento - INTERVAL '1 day' 
                         AND b.data_recebimento + INTERVAL '1 day'
WHERE b.numero_titulo = '54034'
