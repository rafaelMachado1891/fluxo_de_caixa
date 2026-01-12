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

    metrica = plano.get("metrica")
    if metrica not in registry:
        raise ValueError(f"Métrica '{metrica}' não existe.")
    
    parametros_aceitos = registry[metrica].parametros

    plano_filtrado = {
        "metrica": metrica,
        **{k: v for k, v in plano.items() if k in parametros_aceitos}
    }

    return plano_filtrado