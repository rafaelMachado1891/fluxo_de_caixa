from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY")
)

SYSTEM_PROMPT = """
Você é um assistente que interpreta perguntas financeiras.
Retorne APENAS um JSON válido no formato:

{
  "metrica": "saldo_operacional_mes",
  "ano": 2025,
  "mes": 3
}

Regras:
- Use apenas métricas permitidas
- Nunca escreva SQL
- Nunca invente métricas
"""

def interpretar_pergunta(pergunta: str) -> dict:
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": pergunta}
        ],
        temperature=0
    )

    conteudo = resposta.choices[0].message.content.strip()

    try:
        plano = json.loads(conteudo)


    except json.JSONDecodeError:
        raise ValueError(
            f"Resposta inválida do LLM (esperado JSON): {conteudo}"
        )

    if plano.get("metrica") != "saldo_operacional_mes":
        raise ValueError("Métrica não permitida.")

    if not isinstance(plano.get("ano"), int):
        raise ValueError("Ano inválido.")

    if not isinstance(plano.get("mes"), int) or not (1 <= plano["mes"] <= 12):
        raise ValueError("Mês inválido.")

    return plano
