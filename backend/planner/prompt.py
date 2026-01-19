from metricas.base import Metrica

def montar_system_prompt(registry: dict[str, Metrica]) -> str:
    blocos = []

    for m in registry.values():
        bloco = f"""
- nome: {m.nome}
  descricao: {m.descricao}
  dominio: {m.dominio}
  fluxo: {m.fluxo}
  parametros: {", ".join(m.parametros.keys())}
"""
        blocos.append(bloco)

    metricas_texto = "\n".join(blocos)

    return f"""
Você é um assistente que interpreta perguntas financeiras
e escolhe métricas disponíveis.

Siga as regras:
- Escolha UMA métrica
- Nunca invente métricas
- Nunca explique decisões
- Retorne apenas JSON

Métricas disponíveis:
{metricas_texto}

Formato obrigatório:
{{
  "dominio": "<contas|caixa|ranking|outro>",
  "metrica": "<nome>",
  "parametros": {{
    "ano": <int opcional>,
    "mes": <int opcional>
  }}
}}
"""