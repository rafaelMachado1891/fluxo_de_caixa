from metrics import saldo_operacional_mes_atual

def responder(pergunta: str) -> str:
    pergunta = pergunta.lower()

    if "saldo operacional" in pergunta and "mês" in pergunta:
        valor = saldo_operacional_mes_atual()

        valor_decimal = valor[0]

        return (
            f"O saldo operacional realizado no mês atual é R${valor_decimal}"
        )

    return "Ainda não sei responder essa pergunta."