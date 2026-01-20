import time
from metricas.registry import REGISTRY, carregar_metricas
from planner.planner import interpretar_pergunta
from .conversational_agent import AgenteConversacionalLLM
from logs.logger import setup_logger

logger = setup_logger()
carregar_metricas()

_agente = AgenteConversacionalLLM()

def responder_usuario(pergunta: str, contexto=None):

    inicio = time.time()

    logger.info({
        "evento": "pergunta_recebida",
        "pergunta": pergunta
    })

    try:
        # 1. Planejamento
        plano = interpretar_pergunta(pergunta, REGISTRY)

        logger.info({
            "evento": "plano_gerado",
            "metrica": plano.get("metrica"),
            "parametros": plano.get("parametros")
        })

        if not plano.get("metrica"):
            logger.warning({
                "evento": "metrica_nao_identificada",
                "pergunta": pergunta
            })
            return {
                "texto": "Não consegui identificar uma métrica para essa pergunta.",
                "dados": None,
                "metrica": None
            }

        # 2. Execução da métrica
        metrica = REGISTRY[plano["metrica"]]
        params = {k: v for k, v in plano.items() if k != "metrica"}

        resultado = metrica.executar(**params)
        resultado_dict = resultado.model_dump()

        logger.info({
            "evento": "metrica_executada",
            "metrica": plano["metrica"],
            "status": resultado_dict.get("status")
        })

        # 3. Geração da resposta
        resposta = _agente.responder(
            pergunta=pergunta,
            plano=plano,
            resultado=resultado_dict,
            contexto=contexto
        )

        duracao = round(time.time() - inicio, 3)

        logger.info({
            "evento": "resposta_gerada",
            "tempo_execucao_s": duracao
        })

        return {
            "texto": resposta,
            "dados": resultado_dict,
            "metrica": plano["metrica"]
        }

    except Exception as e:
        logger.exception({
            "evento": "erro_no_fluxo",
            "erro": str(e)
        })

        return {
            "texto": "Ocorreu um erro ao processar sua solicitação.",
            "dados": None,
            "metrica": None
        }

