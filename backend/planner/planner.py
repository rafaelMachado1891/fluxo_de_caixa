import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from metricas.base import Metrica
from planner.prompt import montar_system_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))


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

    pergunta_lower = pergunta.lower()

    # ==========================
    # 1️⃣ TENTATIVA POR TAG
    # ==========================
    for nome, metrica in registry.items():
        for tag in getattr(metrica, "tags", []):
            if tag in pergunta_lower:
                return {
                    "metrica": nome,
                    **extrair_parametros(pergunta)
                }

    # ==========================
    # 2️⃣ CHAMADA AO LLM
    # ==========================
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

    try:
        plano = json.loads(conteudo)
    except json.JSONDecodeError:
        return {"metrica": None}

    # ==========================
    # 3️⃣ VALIDAÇÃO SEGURA
    # ==========================
    metrica = plano.get("metrica")

    if not metrica or metrica == "INDETERMINADO":
        return {"metrica": None}

    if metrica not in registry:
        return {"metrica": None}

    return {
        "metrica": metrica,
        **plano.get("parametros", {})
    }


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
