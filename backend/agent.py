from backend.metrics import saldo_operacional_mes_atual

def responder(pergunta: str) -> str:
    pergunta = pergunta.lower()

    if "saldo operacional" in pergunta and "mês" in pergunta:
        valor = saldo_operacional_mes_atual()

        return (
            f"O saldo operacional realizado no mês atual é "
            f"R$ {valor:,.2f}."
        )

    return "Ainda não sei responder essa pergunta."