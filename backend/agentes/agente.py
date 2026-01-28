import time
from metricas.registry import REGISTRY, carregar_metricas
from planner.planner import interpretar_pergunta
from .conversational_agent import AgenteConversacionalLLM
from logs.logger import setup_logger
from analise_causal.analise import analisar_variacoes, extrair_snapshot


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
            return _erro("A pergunta é muito curta ou inválida.")

        termos_validos = [
            "fluxo", "caixa", "saldo",
            "receita", "despesa",
            "lucro", "custo", "faturamento",
            "entradas", "saidas"
        ]

        if not any(t in pergunta.lower() for t in termos_validos):
            return _erro("Só posso responder perguntas relacionadas a métricas financeiras.")

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
            return _erro("Não encontrei uma métrica válida para essa pergunta.")

        # ==========================
        # 3️⃣ EXECUÇÃO DA MÉTRICA
        # ==========================
        metrica = REGISTRY[nome_metrica]
        params = {k: v for k, v in plano.items() if k != "metrica"}

        resultado = metrica.executar(**params)
        resultado_dict = resultado.model_dump()

        # ==========================
        # 4️⃣ ANÁLISE CAUSAL (SE APLICÁVEL)
        # ==========================
        causas = None

        if "mes" in params:
            snapshot_atual = extrair_snapshot(resultado_dict)

            if params.get("mes") > 1:
                resultado_anterior = metrica.executar(
                    ano=params["ano"],
                    mes=params["mes"] - 1
                )
                snapshot_anterior = extrair_snapshot(
                    resultado_anterior.model_dump()
                )
            else:
                snapshot_anterior = None

            causas = analisar_variacoes(
                atual=snapshot_atual,
                anterior=snapshot_anterior
            )

        # ==========================
        # 5️⃣ RESPOSTA DO LLM
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
                "analise": causas,
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

        return _erro("Erro interno ao processar a solicitação.")


# ==========================
# Helpers
# ==========================

def _erro(msg: str):
    return {
        "success": False,
        "message": msg,
        "data": None,
        "meta": {
            "tempo_execucao": 0,
            "fonte": "motor_analitico_v1"
        }
    }