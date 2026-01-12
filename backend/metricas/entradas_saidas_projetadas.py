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
        "saldo operacional",
        "mensal"
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

        return df.to_markdown(index=False)