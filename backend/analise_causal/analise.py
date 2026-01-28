def analisar_variacoes(mes_atual: dict, mes_anterior: dict) -> list[dict]:
    causas = []

    if mes_atual["entradas"] < mes_anterior["entradas"]:
        causas.append({
            "tipo": "queda_entradas",
            "descricao": "Queda nas entradas em relação ao mês anterior",
            "impacto": mes_atual["entradas"] - mes_anterior["entradas"]
        })

    if mes_atual["saidas"] > mes_anterior["saidas"]:
        causas.append({
            "tipo": "aumento_saidas",
            "descricao": "Aumento das saídas em relação ao mês anterior",
            "impacto": mes_atual["saidas"] - mes_anterior["saidas"]
        })

    if mes_atual["saldo_operacional"] < mes_anterior["saldo_operacional"]:
        causas.append({
            "tipo": "queda_saldo",
            "descricao": "Redução do saldo operacional",
            "impacto": mes_atual["saldo_operacional"] - mes_anterior["saldo_operacional"]
        })

    return causas