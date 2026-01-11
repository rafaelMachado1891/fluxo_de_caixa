from metricas.registry import REGISTRY, carregar_metricas
from planner.planner import interpretar_pergunta

carregar_metricas()

def responder(pergunta: str, contexto: dict):
    plano = interpretar_pergunta(pergunta, REGISTRY)

    metrica = REGISTRY[plano["metrica"]]
    resultado = metrica.executar(**plano)
    resposta = metrica.responder(resultado, **plano)

    return resposta, plano