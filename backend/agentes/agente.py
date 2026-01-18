from metricas.registry import REGISTRY, carregar_metricas
from planner.planner import interpretar_pergunta
from .conversational_agent import AgenteConversacionalLLM

carregar_metricas()

# 🔹 criado UMA vez (singleton simples)
_agente = AgenteConversacionalLLM()

def responder_usuario(pergunta: str, contexto: dict | None = None) -> str:
    # 1. Planner
    plano = interpretar_pergunta(pergunta, REGISTRY)

    # 2. Métrica
    metrica = REGISTRY[plano["metrica"]]
    resultado = metrica.executar(**plano)

    # 3. Agente conversacional (reutilizado)
    return _agente.responder(
        pergunta=pergunta,
        plano=plano,
        resultado=resultado,
        contexto=contexto
    )