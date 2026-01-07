from metrics import saldo_operacional_mes, top_5_contas_saidas

CATALOGO_METRICAS= {
    "saldo_operacional_mes": {
        "func": saldo_operacional_mes,
        "descricao": "saldo operacional de um mes especifico",
        "parametro": ["ano", "mes"]
    },
    
    "top_5_contas_saidas": {
        "func": top_5_contas_saidas,
        "descricao": "principais contas que desembolsaram caixa",
        "parametro": ["ano", "mes"]
    }
}