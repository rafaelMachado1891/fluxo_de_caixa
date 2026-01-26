import time
from metricas.registry import REGISTRY, carregar_metricas
from planner.planner import interpretar_pergunta
from .conversational_agent import AgenteConversacionalLLM
from logs.logger import setup_logger
from analise_causal.analise import analisar_variacoes

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
        # ==========================
        # 1️⃣ VALIDAÇÃO
        # ==========================
        if not pergunta or len(pergunta.strip()) < 5:
            return {
                "success": False,
                "message": "A pergunta é muito curta ou inválida.",
                "data": None,
                "meta": {
                    "tempo_execucao": 0,
                    "fonte": "motor_analitico_v1"
                }
            }

        termos_validos = [
            "fluxo", "caixa", "saldo",
            "receita", "despesa",
            "lucro", "custo", "faturamento",
            "entradas", "saidas"
        ]

        if not any(t in pergunta.lower() for t in termos_validos):
            return {
                "success": False,
                "message": "Só posso responder perguntas relacionadas a métricas financeiras.",
                "data": None,
                "meta": {
                    "tempo_execucao": 0,
                    "fonte": "motor_analitico_v1"
                }
            }

        # ==========================
        # 2️⃣ PLANEJAMENTO
        # ==========================
        plano = interpretar_pergunta(pergunta, REGISTRY)

        logger.info({
            "evento": "plano_gerado",
            "plano": plano
        })

        nome_metrica = plano.get("metrica")

        if not nome_metrica or nome_metrica not in REGISTRY:
            return {
                "success": False,
                "message": "Não encontrei uma métrica válida para essa pergunta.",
                "data": None,
                "meta": {
                    "tempo_execucao": 0,
                    "fonte": "motor_analitico_v1"
                }
            }

        # ==========================
        # 3️⃣ EXECUÇÃO
        # ==========================
        metrica = REGISTRY[nome_metrica]
        params = {k: v for k, v in plano.items() if k != "metrica"}

        resultado = metrica.executar(**params)
        resultado_dict = resultado.model_dump()

        causas = None
        
        if "mes" in params:
            mes_atual = resultado_dict
            mes_anterior = metrica.executar(
                ano=params["ano"],
                mes=params["mes"] - 1
            ).model_dump()

            causas = analisar_variacoes(mes_atual=mes_atual,mes_anterior=mes_anterior)

        # ==========================
        # 4️⃣ GERA RESPOSTA
        # ==========================
        resposta = _agente.responder(
            pergunta=pergunta,
            plano=plano,
            resultado=resultado_dict,
            analise=causas,
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

        return {
            "success": False,
            "message": "Erro interno ao processar a solicitação.",
            "data": None,
            "meta": {
                "tempo_execucao": round(time.time() - inicio, 3),
                "fonte": "motor_analitico_v1"
            }
        }

