import time
from metricas.registry import REGISTRY, carregar_metricas
from planner.planner import interpretar_pergunta
from analise_causal.analise import analisar_variacoes
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
        # ==========================
        # 1️⃣ VALIDAÇÃO
        # ==========================
        if not pergunta or len(pergunta.strip()) < 5:
            return _resposta_erro("A pergunta é muito curta ou inválida.", inicio)

        termos_validos = [
            "fluxo", "caixa", "saldo",
            "receita", "despesa", "lucro",
            "custo", "faturamento",
            "entradas", "saidas", "redução",
            "aumento", "queda"
        ]

        if not any(t in pergunta.lower() for t in termos_validos):
            return _resposta_erro(
                "Só posso responder perguntas relacionadas a métricas financeiras.",
                inicio
            )

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
            return _resposta_erro(
                "Não encontrei uma métrica válida para essa pergunta.",
                inicio
            )

        # ==========================
        # 3️⃣ EXECUÇÃO DA MÉTRICA
        # ==========================
        metrica = REGISTRY[nome_metrica]
        params = {k: v for k, v in plano.items() if k != "metrica"}

        resultado = metrica.executar(**params)
        resultado_dict = resultado.model_dump()

        # ==========================
        # 4️⃣ ANÁLISE (OPCIONAL)
        # ==========================
        causas = None

        detalhes = resultado_dict.get("detalhes")

        if detalhes and "mes" in params:
            try:
                resultado_anterior = metrica.executar(
                    ano=params["ano"],
                    mes=params["mes"] - 1
                ).model_dump()

                detalhes_anterior = resultado_anterior.get("detalhes")

                if detalhes_anterior:
                    causas = analisar_variacoes(
                        mes_atual=detalhes,
                        mes_anterior=detalhes_anterior
                    )
            except Exception as e:
                logger.warning({
                    "evento": "falha_analise_variacao",
                    "erro": str(e)
                })

        # ==========================
        # 5️⃣ GERA RESPOSTA
        # ==========================
        resposta = _agente.responder(
            pergunta=pergunta,
            plano=plano,
            resultado=resultado_dict,
            analise=causas,
            contexto=contexto
        )

        return {
            "success": True,
            "message": resposta,
            "data": {
                "metrica": nome_metrica,
                "resultado": resultado_dict,
                "detalhes": resultado_dict.get("detalhes"),
                "analise": causas
            },
            "meta": {
                "tempo_execucao": round(time.time() - inicio, 3),
                "fonte": "motor_analitico_v1"
            }
        }

    except Exception as e:
        logger.exception({
            "evento": "erro_no_fluxo",
            "erro": str(e)
        })

        return _resposta_erro("Erro interno ao processar a solicitação.", inicio)


# ============================================================
# FUNÇÃO AUXILIAR (evita repetição)
# ============================================================
def _resposta_erro(mensagem: str, inicio: float):
    return {
        "success": False,
        "message": mensagem,
        "data": None,
        "meta": {
            "tempo_execucao": round(time.time() - inicio, 3),
            "fonte": "motor_analitico_v1"
        }
    }