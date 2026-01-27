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
Você é um agente especializado EXCLUSIVAMENTE em interpretação de métricas financeiras.

Sua função é analisar a pergunta do usuário e retornar um JSON que identifique:
- qual métrica deve ser usada
- quais parâmetros devem ser aplicados

⚠️ REGRAS OBRIGATÓRIAS:
- Responda APENAS com JSON válido.
- NÃO escreva explicações, textos ou comentários fora do JSON.
- NÃO invente métricas.
- NÃO invente parâmetros.
- NÃO responda perguntas fora do domínio financeiro.
- Se nenhuma métrica for compatível, retorne o JSON de fallback abaixo.
- Sempre respeite exatamente o formato solicitado.
- Se houver lista de causas, explique-as de forma clara.

📌 MÉTRICAS DISPONÍVEIS:
{metricas_texto}

📌 FORMATO DE SAÍDA (OBRIGATÓRIO):
{{
  "dominio": "<contas|caixa|ranking|outro>",
  "metrica": "<nome_da_metrica_ou_null>",
  "parametros": {{
    "ano": <int ou null>,
    "mes": <int ou null>
  }}
}}

📌 FORMATO DE FALLBACK (se não houver métrica válida):
{{
  "dominio": null,
  "metrica": null,
  "parametros": {{}}
}}
"""