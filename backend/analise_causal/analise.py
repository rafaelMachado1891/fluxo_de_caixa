def analisar_variacoes(mes_atual: int, mes_anterior: int) -> list[dict]:
    causas = []

    if mes_atual.receitas < mes_anterior.receitas:
        causas.append({
            "tipo": "queda na receita",
            "impacto": mes_atual.receitas - mes_anterior.receitas
        })

    if mes_atual.despesas > mes_anterior.despesas:
        causas.append({
            "tipo": "aumento das despesas",
            "impacto": mes_atual.despesas - mes_anterior.despesas
        })

    return causas