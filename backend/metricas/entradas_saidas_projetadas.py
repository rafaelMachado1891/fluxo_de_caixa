from metrics import calcular_total_saida_entradas_por_semana
from metricas.base import Metrica
import pandas as pd
import tabulate

class EntradasSaidasProjetadas(Metrica):
    nome = "total de entradas e saídas por semana"
    descricao = "calcula entradas, saídas e saldo operacional por semana"
    
    parametros = ["ano", "mes"]
    parametros_obrigatorios = []  # 👈 NENHUM obrigatório

    dominio = "caixa"
    fluxo = "projetado"
    tags = [
        "saidas",
        "entradas",
        "saldo operacional",
        "pagamento",
        "recebimento"
    ]

    def executar(self, **kwargs):
        self.validar_parametros(**kwargs)

        return calcular_total_saida_entradas_por_semana(
            ano=kwargs.get("ano"),
            mes=kwargs.get("mes")
        )

    def responder(self, resultado, **kwargs) -> str:
        df = pd.DataFrame(resultado)

        if df.empty:
            return "⚠️ Não há dados projetados para o período informado."

        df["ano_mes"] = df["ano_mes"].astype(str)
        df["semana_ano"] = df["semana_ano"].astype(int)
        df["entradas"] = df["entradas"].astype(float)
        df["saidas"] = df["saidas"].astype(float)
        df["saldo_operacional"] = df["saldo_operacional"].astype(float)

        tabela = df.copy()
        tabela[["entradas", "saidas", "saldo_operacional"]] = (
            tabela[["entradas", "saidas", "saldo_operacional"]]
            .applymap(lambda x: f"{x:,.2f}")
        )

        markdown = tabela.to_markdown(index=False)

        mes = kwargs.get("mes")
        ano = kwargs.get("ano")

        periodo = f"{mes:02d}/{ano}" if mes and ano else "semana atual"