from metrics import saldo_operacional_mes

CATALOGO_METRICAS= {
    "saldo_operacional_mes": {
        "func": saldo_operacional_mes,
        "descricao": "saldo operacional de um mes especifico",
        "parametro": ["ano", "mes"]
    }
}