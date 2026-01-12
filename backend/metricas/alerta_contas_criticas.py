from metrics import alerta_contas_criticas
from metricas.base import Metrica
import pandas as pd

class AlertaContasCriticas(Metrica):
    nome = "alerta_desvio_contas_projetado"
    descricao = (
    "Alerta de contas com saídas projetadas acima do padrão histórico "
    "(desvio em relação à média móvel)"
    )

    palavras_chave = [
    "alerta",
    "desvio",
    "acima da média",
    "fora do padrão",
    "projetado",
    "risco",
    "anômalo,"
    "contas criticas"
    ]
    parametros = [] 

    dominio = ""

    def executar(self, **kwargs):
        return alerta_contas_criticas()

    def responder(self, resultado, **kwargs):
        import pandas as pd

        if not resultado:
            return (
                "### 📊 Contas Críticas\n\n"
                "Nenhuma conta apresentou saídas projetadas acima da média histórica."
            )

        df = pd.DataFrame(resultado)

        df["total_saidas_projetadas"] = df["total_saidas_projetadas"].astype(float)
        df["media_movel_3m"] = df["media_movel_3m"].astype(float)
        df["desvio"] = df["desvio"].astype(float)

        df[["total_saidas_projetadas", "media_movel_3m", "desvio"]] = df[
            ["total_saidas_projetadas", "media_movel_3m", "desvio"]
        ].applymap(lambda x: f"{x:,.2f}")

        tabela = df.rename(columns={
            "conta_contabil": "Conta Contábil",
            "total_saidas_projetadas": "Saídas Projetadas (R$)",
            "media_movel_3m": "Média 3M (R$)",
            "desvio": "Desvio (R$)"
        }).to_string(index=False)

        return (
            "### 📊 Contas Críticas\n\n"
            f"{tabela}"
        )