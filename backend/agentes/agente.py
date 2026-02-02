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

    logger.info({
        "evento": "pergunta_recebida",
        "pergunta": pergunta,
        "contexto": contexto
    })

    try:
        if not pergunta or len(pergunta.strip()) < 5:
            logger.warning({
                "evento": "pergunta_invalida",
                "pergunta": pergunta
            })

            return ApiResponse(
                success=False,
                status="erro",
                message="A pergunta é muito curta ou inválida.",
                data=None,
                meta=ApiMeta(tempo_execucao=0)
            )

        plano = interpretar_pergunta(pergunta, REGISTRY)

        logger.info({
            "evento": "plano_interpretado",
            "plano": plano
        })

        plano = resolver_contexto(plano, contexto)

        logger.info({
            "evento": "plano_apos_contexto",
            "plano": plano
        })

        nome_metrica = plano.get("metrica")
        if not nome_metrica or nome_metrica not in REGISTRY:

            logger.info({
                "evento": "metrica_nao_encontrada",
                "plano": plano
            })

            return ApiResponse(
                success=False,
                status="erro",
                message="Não encontrei uma métrica válida para essa pergunta.",
                data=None,
                meta=ApiMeta(tempo_execucao=0)
            )
        
        logger.info({
            "evento": "metrica_selecionada",
            "plano": plano
        })

        metrica = REGISTRY[nome_metrica]
        params = {k: v for k, v in plano.items() if k != "metrica"}

        logger.info({
            "evento": "executando_metrica",
            "parametros": params
        })

        resultado = metrica.executar(**params)

        logger.info({
            "evento": "metrica_executada",
            "resultado": resultado.dict()
        })

        visualizacao = decidir_visualizacao(resultado)

        logger.info({
            "evento": "escolher_visualizacao",
            "visualizacao": visualizacao
        })

        texto = _agente.responder(
            pergunta=pergunta,
            plano=plano,
            resultado=resultado,
            contexto=contexto
        )

        logger.info({
            "evento": "resposta_gerada",
            "resposta": texto[:120]
        })

        

        return ApiResponse(
            success=True,
            status="ok",
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
        logger.exception({
            "evento": "erro_no_fluxo",
            "erro": str(e)
        })

        return ApiResponse(
            success=False,
            status="erro",
            message="Erro interno ao processar a solicitação.",
            data=None,
            meta=ApiMeta(tempo_execucao=round(time.time() - inicio, 3))
        )