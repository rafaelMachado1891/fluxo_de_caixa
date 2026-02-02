import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from metricas.base import Metrica
from planner.prompt import montar_system_prompt
from logs.logger import setup_logger



load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))

logger = setup_logger()


def interpretar_pergunta(
    pergunta: str,
    registry: dict[str, Metrica],
    contexto: dict | None = None
) -> dict:
    """
    Interpreta a pergunta do usuário.

    Regras:
    - Primeiro tenta resolver por tags
    - Depois tenta usar o LLM
    - Nunca lança exceção
    - Nunca retorna metrica inválida
    """
    logger.info({
        "evento": "planner_inicio",
        "pergunta": pergunta,
        "contexto": contexto
    })

    pergunta_lower = pergunta.lower()

    termos_variacao = [
        "aumentou", "reduziu", "diminuiu", "cresceu",
        "piorou", "melhorou", "comparado",
        "em relação", "variação", "aumentaram", "diminuiram"
    ]

    # =====================================================
    # 1️⃣ REGRA ABSOLUTA: VARIAÇÃO
    # =====================================================
    if any(t in pergunta_lower for t in termos_variacao):
        logger.info({
            "evento": "detecao_variacao",
            "motivo": "termo_detectado"
        })

        if contexto and contexto.get("ultima_metrica"):
            plano = {
                "metrica": "análise de variação do fluxo de caixa",
                "ano": contexto.get("ultimo_ano"),
                "mes": contexto.get("ultimo_mes")
            }

            logger.info({
                "evento": "plano_variacao",
                "plano": plano
            })

            return plano

        # fallback se não houver contexto
        logger.warning({
            "evento": "variacao_sem_contexto"
        })

        return {
            "metrica": "análise de variação do fluxo de caixa"
        }

    # =====================================================
    # 2️⃣ BUSCA POR TAG (SÓ SE NÃO FOR VARIAÇÃO)
    # =====================================================
    for nome, metrica in registry.items():
        for tag in getattr(metrica, "tags", []):
            if tag in pergunta_lower:
                plano = {
                    "metrica": nome,
                    **extrair_parametros(pergunta)
                }

                logger.info({
                    "evento": "plano_por_tag",
                    "tag": tag,
                    "plano": plano
                })

                return plano
            

    logger.info({
        "evento": "fallback_llm",
        "motivo": "nenhuma_tag_encontrada"
    })

 
    system_prompt = montar_system_prompt(registry)

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pergunta}
        ],
        temperature=0
    )

    conteudo = resposta.choices[0].message.content.strip()

    logger.info({
        "evento": "resposta_llm",
        "conteudo_bruto": conteudo
    })

    try:
        plano = json.loads(conteudo)

    except json.JSONDecodeError:

        logger.error({
            "evento": "erro_json_llm",
            "conteudo": conteudo
        })

        return {"metrica": None}

    # ==========================
    # 3️⃣ VALIDAÇÃO SEGURA
    # ==========================
    metrica = plano.get("metrica")

    if not metrica or metrica == "INDETERMINADO":

        logger.warning({
            "evento": "metrica_indeterminada",
            "plano": plano
        })

        return {"metrica": None}

    if metrica not in registry:

        logger.warning({
            "evento": "metrica_invalida",
            "metrica": metrica
        })

        return {"metrica": None}

    plano_final =  {
        "metrica": metrica,
        **plano.get("parametros", {})
    }

    logger.info({
        "evento": "plano_final",
        "plano": plano_final
    })

    return plano_final


def extrair_parametros(pergunta: str) -> dict:
    """
    Extrai ano e mês de forma simples.
    Pode evoluir depois.
    """
    import re
    from datetime import datetime

    ano = None
    mes = None

    ano_match = re.search(r"(20\d{2})", pergunta)
    if ano_match:
        ano = int(ano_match.group(1))

    meses = {
        "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4,
        "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
        "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
    }

    for nome, numero in meses.items():
        if nome in pergunta.lower():
            mes = numero
            break

    if not ano:
        ano = datetime.now().year

    return {
        "ano": ano,
        "mes": mes
    }
