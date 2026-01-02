from catalogo import CATALOGO_METRICAS
from planner import interpretar_pergunta

def responder(pergunta: str) -> str:
    plano = interpretar_pergunta(pergunta)

    metrica_nome = plano["metrica"]

    if metrica_nome not in CATALOGO_METRICAS:
        return "Ainda não sei responder essa pergunta."

    metrica = CATALOGO_METRICAS[metrica_nome]
    func = metrica["func"]

    valor = func(
        ano=plano["ano"],
        mes=plano["mes"]
    )

    return (
        f"O saldo operacional realizado em "
        f"{plano['mes']:02d}/{plano['ano']} foi "
        f"R$ {valor:,.2f}."
    )