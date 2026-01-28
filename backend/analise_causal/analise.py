from models.schema import SnapshotFinanceiro
from typing import List


def extrair_snapshot(resultado: dict):
    detalhes = resultado.get("detalhes")

    if not detalhes:
        return None

    return {
        "entradas": detalhes.get("entradas"),
        "saidas": detalhes.get("saidas"),
        "saldo_operacional": detalhes.get("saldo_operacional")
    }


def analisar_variacoes(atual, anterior):
    causas = []

    if not atual or not anterior:
        return causas

    if atual.get("entradas") is not None and anterior.get("entradas") is not None:
        if atual["entradas"] < anterior["entradas"]:
            causas.append({
                "tipo": "queda_receita",
                "impacto": atual["entradas"] - anterior["entradas"]
            })

    if atual.get("saidas") is not None and anterior.get("saidas") is not None:
        if atual["saidas"] > anterior["saidas"]:
            causas.append({
                "tipo": "aumento_despesas",
                "impacto": atual["saidas"] - anterior["saidas"]
            })

    if (
        atual.get("saldo_operacional") is not None and
        anterior.get("saldo_operacional") is not None and
        atual["saldo_operacional"] < anterior["saldo_operacional"]
    ):
        causas.append({
            "tipo": "queda_saldo",
            "impacto": atual["saldo_operacional"] - anterior["saldo_operacional"]
        })

    return causas