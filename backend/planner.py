from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from catalogo import CATALOGO_METRICAS

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"))

SYSTEM_PROMPT = """
Você é um assistente que interpreta perguntas financeiras.

Retorne APENAS um JSON válido seguindo UM dos formatos abaixo.

Formato 1 — quando a pergunta citar mês e ano:
{
  "metrica": "saldo_operacional_mes",
  "ano": 2025,
  "mes": 3
}

Formato 2 — quando a pergunta NÃO citar mês e ano:
{
  "metrica": "top_5_contas_saidas"
}

Regras obrigatórias:
- Use apenas métricas permitidas
- Nunca escreva SQL
- Nunca invente métricas
- Nunca inclua texto fora do JSON
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
        raise ValueError("Não consegui interpretar sua pergunta.")

    # 🔒 valida SOMENTE a métrica
    metrica = plano.get("metrica")
    if metrica not in CATALOGO_METRICAS:
        raise ValueError("Não sei responder essa pergunta ainda.")

    # valida ano se existir
    if "ano" in plano and not isinstance(plano["ano"], int):
        raise ValueError("Ano inválido.")

    # valida mês se existir
    if "mes" in plano:
        mes = plano["mes"]
        if not isinstance(mes, int) or not (1 <= mes <= 12):
            raise ValueError("Mês inválido.")

    return plano
