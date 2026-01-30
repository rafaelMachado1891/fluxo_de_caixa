import time
from metricas.registry import REGISTRY, carregar_metricas
from planner.planner import interpretar_pergunta
from .conversational_agent import AgenteConversacionalLLM
from logs.logger import setup_logger
from models.schema import ApiResponse, ApiMeta, ApiData
from agentes.visualizacao import decidir_visualizacao


logger = setup_logger()
carregar_metricas()

_agente = AgenteConversacionalLLM()


def resolver_contexto(plano: dict, contexto: dict | None):
    """
    Resolve perguntas implícitas como:
    'melhorou?', 'piorou?', 'aumentou?'
    usando o último contexto válido.
    """
    if plano.get("metrica"):
        return plano

    if not contexto:
        return plano

    ultima_metrica = contexto.get("ultima_metrica")
    ultimo_mes = contexto.get("ultimo_mes")
    ultimo_ano = contexto.get("ultimo_ano")

    if not ultima_metrica:
        return plano

    # assume que perguntas sem métrica são comparações
    return {
        "metrica": f"variacao_{ultima_metrica}",
        "ano": ultimo_ano,
        "mes": ultimo_mes
    }


def atualizar_contexto(contexto: dict, plano: dict):
    """Salva o estado da conversa"""
    if contexto is None:
        return

    contexto["ultima_metrica"] = plano.get("metrica")
    contexto["ultimo_ano"] = plano.get("ano")
    contexto["ultimo_mes"] = plano.get("mes")


def responder_usuario(pergunta: str, contexto: dict | None = None):
    inicio = time.time()

    try:
        if not pergunta or len(pergunta.strip()) < 5:
            return ApiResponse(
                success=False,
                status="erro",
                message="A pergunta é muito curta ou inválida.",
                data=None,
                meta=ApiMeta(tempo_execucao=0)
            )

        plano = interpretar_pergunta(pergunta, REGISTRY)
        plano = resolver_contexto(plano, contexto)

        nome_metrica = plano.get("metrica")
        if not nome_metrica or nome_metrica not in REGISTRY:
            return ApiResponse(
                success=False,
                status="erro",
                message="Não encontrei uma métrica válida para essa pergunta.",
                data=None,
                meta=ApiMeta(tempo_execucao=0)
            )

        metrica = REGISTRY[nome_metrica]
        params = {k: v for k, v in plano.items() if k != "metrica"}

        resultado = metrica.executar(**params)

        visualizacao = decidir_visualizacao(resultado)

        texto = _agente.responder(
            pergunta=pergunta,
            plano=plano,
            resultado=resultado,
            contexto=contexto
        )

        status = "ok" if resultado.valor is not None else "sem_dados"

        return ApiResponse(
            success=status == "ok",
            status=status,
            message=texto,
            data=ApiData(
                resultado=resultado,
                visualizacao=visualizacao
            ),
            meta=ApiMeta(
                tempo_execucao=round(time.time() - inicio, 3)
            )
        )

    except Exception as e:
        logger.exception("Erro no fluxo")

        return ApiResponse(
            success=False,
            status="erro",
            message="Erro interno ao processar a solicitação.",
            data=None,
            meta=ApiMeta(tempo_execucao=round(time.time() - inicio, 3))
        )