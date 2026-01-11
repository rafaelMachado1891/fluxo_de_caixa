from metricas.base import Metrica

def montar_system_prompt(registry: dict[str, Metrica]) -> str:
    blocos = []

    for m in registry.values():
        bloco = f"""
- nome: {m.nome}
  descricao: {m.descricao}
  palavras_chave: {", ".join(m.palavras_chave)}
  parametros: {", ".join(m.parametros)}
"""
        blocos.append(bloco)

    metricas_texto = "\n".join(blocos)

    return f"""
Você é um assistente que interpreta perguntas financeiras.

Escolha a métrica MAIS adequada com base no significado da pergunta.

Métricas disponíveis:
{metricas_texto}

Retorne APENAS um JSON válido no formato:

{{
  "metrica": "<nome_da_metrica>",
  "ano": 2025,
  "mes": 3
}}

Regras obrigatórias:
- Use somente métricas listadas
- Se a pergunta mencionar projeção, futuro ou previsto, use métricas projetadas
- Nunca escreva SQL
- Nunca escreva texto fora do JSON
"""