from openai import OpenAI
import json
import os
from dotenv import load_dotenv

from planner.prompt import montar_system_prompt
from metricas.base import Metrica


load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))


def interpretar_pergunta(pergunta: str, registry: dict[str, Metrica]) -> dict:
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
        raise ValueError("Planner retornou JSON inválido.")

    # 🔒 valida métrica
    metrica = plano.get("metrica")
    if metrica not in registry:
        raise ValueError(f"Métrica '{metrica}' não existe.")

    # 🔒 valida parâmetros esperados
    parametros_esperados = registry[metrica].parametros
    for p in parametros_esperados:
        if p not in plano:
            raise ValueError(f"Parâmetro '{p}' ausente para a métrica '{metrica}'.")

    return plano