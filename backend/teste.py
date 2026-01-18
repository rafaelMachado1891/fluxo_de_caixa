from agentes.agente import responder_usuario   # ajuste o import se o arquivo tiver outro nome

if __name__ == "__main__":
    pergunta = "Qual foi o saldo final projetado de janeiro de 2026?"
    resposta = responder_usuario(pergunta)
    print(resposta)