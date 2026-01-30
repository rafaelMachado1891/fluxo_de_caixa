import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from utils_db import normalizar_para_json

load_dotenv()
_client = OpenAI(api_key=os.getenv("API_KEY"))


class AgenteConversacional:
    def responder(self, pergunta, plano, resultado, contexto=None):
        """
        Fallback sem LLM.
        Usa apenas dados estruturados.
        """
        if resultado.valor is None:
            return self._resposta_sem_dados(resultado)

        return self._resposta_ok(resultado)

    def _resposta_sem_dados(self, resultado):
        periodo = self._formatar_periodo(resultado)
        return f"⚠️ Não há dados disponíveis para {periodo}."

    def _resposta_ok(self, resultado):
        valor = resultado.valor
        unidade = resultado.unidade
        metrica = resultado.metrica
        periodo = self._formatar_periodo(resultado)

        valor_fmt = self._formatar_valor(valor, unidade)

        resposta = (
            f"## {metrica.title()}\n"
            f"📅 **Período:** {periodo}\n\n"
            f"O valor apurado foi **{valor_fmt}**."
        )

        if resultado.detalhes:
            resposta += self._renderizar_detalhes(resultado.detalhes)

        return resposta

    def _formatar_periodo(self, resultado):
        if resultado.mes and resultado.ano:
            return f"{resultado.mes:02d}/{resultado.ano}"
        if resultado.ano:
            return str(resultado.ano)
        return "período atual"

    def _formatar_valor(self, valor, unidade):
        if unidade == "BRL":
            return f"R$ {valor:,.2f}"
        if unidade == "%":
            return f"{valor:.2f}%"
        return str(valor)

    def _renderizar_detalhes(self, detalhes):
        linhas = []

        if "entradas_total" in detalhes:
            linhas.append(f"- 💰 Entradas: R$ {detalhes['entradas_total']:,.2f}")
        if "saidas_total" in detalhes:
            linhas.append(f"- 💸 Saídas: R$ {detalhes['saidas_total']:,.2f}")

        if not linhas:
            return ""

        return "\n\n### 🔎 Detalhamento\n" + "\n".join(linhas)
    

class AgenteConversacionalLLM(AgenteConversacional):

    def responder(self, pergunta, plano, resultado, analise=None, contexto=None):
        prompt = self._montar_prompt(pergunta, plano, resultado, analise, contexto)
        try:
            return self._chamar_llm(prompt)
        except Exception:
            return super().responder(pergunta, plano, resultado, contexto)

    def _montar_prompt(self, pergunta, plano, resultado, analise=None, contexto=None):
        resultado_json = resultado.model_dump(mode="json")

        return f"""
Você é um assistente financeiro.

Use SOMENTE os dados abaixo.

Pergunta:
{pergunta}

Plano:
{json.dumps(plano, ensure_ascii=False, indent=2)}

Resultado:
{json.dumps(resultado_json, ensure_ascii=False, indent=2)}

Explique de forma clara e objetiva.
"""

    def _chamar_llm(self, prompt: str) -> str:
        resp = _client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return resp.choices[0].message.content.strip()