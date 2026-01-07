from catalogo import CATALOGO_METRICAS
from planner import interpretar_pergunta

def responder(pergunta: str, contexto: dict) -> tuple[str, dict]:
    plano = interpretar_pergunta(pergunta)

    # 🔁 Herda contexto se não vier do LLM
    ano = plano.get("ano") or contexto.get("ano")
    mes = plano.get("mes") or contexto.get("mes")

    if ano is None or mes is None:
        return (
            "Para responder, preciso saber o mês e o ano.",
            contexto
        )

    metrica_nome = plano["metrica"]

    if metrica_nome not in CATALOGO_METRICAS:
        return ("Ainda não sei responder essa pergunta.", contexto)

    func = CATALOGO_METRICAS[metrica_nome]["func"]

    resultado = func(ano=ano, mes=mes)

    # Atualiza contexto
    novo_contexto = {
        "ano": ano,
        "mes": mes
    }

    # 🔍 Respostas diferentes por métrica
    if metrica_nome == "saldo_operacional_mes":
        resposta = (
            f"O saldo operacional realizado em "
            f"{mes:02d}/{ano} foi R$ {resultado:,.2f}."
        )

    elif metrica_nome == "top_5_contas_saidas":
        if not resultado:
            resposta = "Não encontrei saídas para esse período."
        else:
            linhas = [
                f"- {r['conta_contabil']}: R$ {r['valor_total']:,.2f}"
                for r in resultado
            ]
            resposta = (
                f"As contas que mais impactaram o caixa em "
                f"{mes:02d}/{ano} foram:\n" + "\n".join(linhas)
            )

    return resposta, novo_contexto