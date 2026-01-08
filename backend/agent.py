from metricas.registry import REGISTRY, carregar_metricas
from planner import interpretar_pergunta

carregar_metricas()

def responder(pergunta: str, contexto: dict) -> tuple[str, dict]:
    plano = interpretar_pergunta(pergunta)

    ano = plano.get("ano") or contexto.get("ano")
    mes = plano.get("mes") or contexto.get("mes")

    if ano is None or mes is None:
        return "Para responder, preciso saber o mês e o ano.", contexto

    metrica = REGISTRY.get(plano["metrica"])

    if not metrica:
        return "Ainda não sei responder essa métrica.", contexto

    resultado = metrica.executar(ano=ano, mes=mes)
    resposta = metrica.responder(resultado, ano=ano, mes=mes)

    return resposta, {"ano": ano, "mes": mes}