from metricas.registry import REGISTRY, carregar_metricas
from planner.planner import interpretar_pergunta
from .conversational_agent import AgenteConversacionalLLM

carregar_metricas()

# 🔹 criado UMA vez (singleton simples)
_agente = AgenteConversacionalLLM()

def responder_usuario(pergunta: str, contexto=None):

    plano = interpretar_pergunta(pergunta, REGISTRY)

    if not plano.get("metrica"):
        return "Não consegui identificar uma métrica para essa pergunta."

    metrica = REGISTRY[plano["metrica"]]

    params = {k: v for k, v in plano.items() if k != "metrica"}

    resultado = metrica.executar(**params)
    resultado_dict = resultado.model_dump()

    resposta = _agente.responder(
        pergunta=pergunta,
        plano=plano,
        resultado=resultado_dict,
        contexto=contexto
    )

    return resposta


