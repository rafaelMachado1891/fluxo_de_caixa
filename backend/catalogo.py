from metrics import saldo_operacional_mes_atual

catalago = {
    "saldo_operacional_mes": {
        "funcao": saldo_operacional_mes_atual,
        "descricao": "saldo operacional de um mes especifico",
        "parametro": ["ano", "mes"]
    }
}