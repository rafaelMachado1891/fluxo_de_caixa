import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from utils_db import normalizar_para_json

load_dotenv()
_client = OpenAI(api_key=os.getenv("API_KEY"))


class AgenteConversacional:
    def responder(self, pergunta, plano, resultado, contexto=None, analise=None):
        status = resultado["status"]

        if status == "sem_dados":
            return self._resposta_sem_dados(resultado)

        if status == "erro":
            return "⚠️ Ocorreu um erro ao calcular a métrica."

        return self._resposta_ok(resultado)

    def _resposta_sem_dados(self, resultado):
        periodo = self._formatar_periodo(resultado)
        return f"⚠️ Não há dados disponíveis para {periodo}."

    def _resposta_ok(self, resultado):
        valor = resultado["valor"]
        unidade = resultado["unidade"]
        metrica = resultado["metrica"]
        periodo = self._formatar_periodo(resultado)

        valor_fmt = self._formatar_valor(valor, unidade)

        resposta = (
            f"## {metrica.title()}\n"
            f"📅 **Período:** {periodo}\n\n"
            f"O valor apurado foi **{valor_fmt}**."
        )

        if resultado.get("detalhes"):
            resposta += self._renderizar_detalhes(resultado["detalhes"])

        return resposta

    def _formatar_periodo(self, resultado):
        mes = resultado.get("mes")
        ano = resultado.get("ano")

        if mes and ano:
            return f"{mes:02d}/{ano}"
        if ano:
            return str(ano)

        return "período atual"

    def _formatar_valor(self, valor, unidade):
        if unidade == "BRL":
            return f"R$ {valor:,.2f}"
        if unidade == "%":
            return f"{valor:.2f}%"
        return str(valor)

    def _renderizar_detalhes(self, detalhes):
        linhas = []

        if "entradas" in detalhes:
            linhas.append(f"- 💰 Entradas: R$ {detalhes['entradas']:,.2f}")
        if "saidas" in detalhes:
            linhas.append(f"- 💸 Saídas: R$ {detalhes['saidas']:,.2f}")

        if not linhas:
            return ""

        return "\n\n### 🔎 Detalhamento\n" + "\n".join(linhas)


# ======================================================
# AGENTE COM IA (ÚNICO!)
# ======================================================

class AgenteConversacionalLLM(AgenteConversacional):

    def responder(self, pergunta, plano, resultado, analise=None, contexto=None):
        try:
            prompt = self._montar_prompt(
                pergunta=pergunta,
                plano=plano,
                resultado=resultado,
                analise=analise
            )
            return self._chamar_llm(prompt)
        except Exception:
            return super().responder(pergunta, plano, resultado, contexto, analise)

    def _montar_prompt(self, pergunta, plano, resultado, analise=None):

        resultado_json = normalizar_para_json(resultado)

        prompt = f"""
Você é um analista financeiro.

Use SOMENTE os dados abaixo para responder.

Pergunta:
{pergunta}

Plano:
{json.dumps(plano, ensure_ascii=False, indent=2)}

Resultado:
{json.dumps(resultado_json, ensure_ascii=False, indent=2)}
"""

        if analise:
            prompt += f"""

Análise encontrada:
{json.dumps(analise, ensure_ascii=False, indent=2)}

Explique os resultados considerando essas variações.
"""

        return prompt

    def _chamar_llm(self, prompt: str) -> str:
        resp = _client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return resp.choices[0].message.content.strip()