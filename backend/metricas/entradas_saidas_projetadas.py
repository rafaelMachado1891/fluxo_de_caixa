from metricas.base import Metrica
from metrics import calcular_total_entradas_saidas_por_mes
import pandas as pd


class EntradasSaidasProjetadas(Metrica):
    nome = "total de entradas e saídas por mês"
    descricao = "Entradas, saídas e saldo operacional do mês"
    dominio = "caixa"
    fluxo = "projetado"

    tags = [
        "entradas",
        "saidas",
        "mensal",
        "receber",
        "pagar"
    ]

    parametros = {
        "ano": {"tipo": int},
        "mes": {"tipo": int}
    }

    def executar(self, **kwargs):
        return calcular_total_entradas_saidas_por_mes(
            ano=kwargs.get("ano"),
            mes=kwargs.get("mes")
        )

    def responder(self, resultado, **kwargs) -> str:
        df = pd.DataFrame(resultado)

        if df.empty:
            return "⚠️ Não há dados projetados para o período informado."
        
        mes = kwargs.get("mes", "mês atual")
        ano = kwargs.get("ano", "ano atual")

        cabecalho = (
            f"## 💰 Entradas e Saídas Projetadas\n"
            f"📅 **Período:** {mes}/{ano}\n\n"
        )

        tabela = df.to_markdown(index=False)

        return f"{cabecalho}{tabela}"