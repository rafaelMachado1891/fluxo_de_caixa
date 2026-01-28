import time
from metricas.registry import REGISTRY, carregar_metricas
from planner.planner import interpretar_pergunta
from .conversational_agent import AgenteConversacionalLLM
from logs.logger import setup_logger


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
        "pergunta": pergunta
    })

    try:
        # ==========================
        # 1️⃣ VALIDAÇÃO
        # ==========================
        if not pergunta or len(pergunta.strip()) < 5:
            return "A pergunta é muito curta ou inválida."

        # ==========================
        # 2️⃣ PLANEJAMENTO
        # ==========================
        plano = interpretar_pergunta(pergunta, REGISTRY)

        # 🧠 Resolve contexto implícito
        plano = resolver_contexto(plano, contexto)

        logger.info({
            "evento": "plano_resolvido",
            "plano": plano
        })

        nome_metrica = plano.get("metrica")
        if not nome_metrica or nome_metrica not in REGISTRY:
            return "Não encontrei uma métrica válida para essa pergunta."

        # ==========================
        # 3️⃣ EXECUÇÃO DA MÉTRICA
        # ==========================
        metrica = REGISTRY[nome_metrica]
        params = {k: v for k, v in plano.items() if k != "metrica"}

        resultado = metrica.executar(**params)
        resultado_dict = resultado.model_dump()

        logger.info({
            "evento": "metrica_executada",
            "metrica": nome_metrica,
            "resultado": resultado_dict
        })

        # ==========================
        # 4️⃣ ATUALIZA CONTEXTO
        # ==========================
        atualizar_contexto(contexto, plano)

        # ==========================
        # 5️⃣ RESPOSTA DO LLM
        # ==========================
        resposta = _agente.responder(
            pergunta=pergunta,
            plano=plano,
            resultado=resultado_dict,
            contexto=contexto
        )

        duracao = round(time.time() - inicio, 3)

        return {
            "success": True,
            "message": resposta,
            "data": {
                "metrica": nome_metrica,
                "resultado": resultado_dict,
                "detalhes": resultado_dict.get("detalhes")
            },
            "meta": {
                "tempo_execucao": duracao,
                "fonte": "motor_analitico_v1"
            }
        }

    except Exception as e:
        logger.exception({
            "evento": "erro_no_fluxo",
            "erro": str(e)
        })

        return "Erro interno ao processar a solicitação."