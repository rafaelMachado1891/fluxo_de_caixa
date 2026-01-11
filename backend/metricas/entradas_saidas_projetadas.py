from metrics import entradas_saidas_projetadas
from metricas.base import Metrica
import pandas as pd
import tabulate

class Entradas_Saidas_Projetadas(Metrica):
    nome = "entradas_saidas_projetadas"
    descricao = "tota de saidas e entradas projetadas agrupadas por mes e semana"
    palavras_chave = ["saídas", "entradas", "projetadas", "futuras"]
    parametros = ["ano","mes"]

    def executar(self, **kwargs):
        return entradas_saidas_projetadas(
            ano=kwargs["ano"],
            mes=kwargs["mes"]
        )
    
    def responder(self, resultado, **kwargs) -> str:
        # cria DataFrame
        df = pd.DataFrame(resultado)

        # normaliza tipos
        df["week_of_year"] = df["week_of_year"].astype(int)
        df["valor"] = df["valor"].astype(float)

        # pivota Entradas (E) e Saídas (S)
        tabela = (
            df.pivot_table(
                index="week_of_year",
                columns="tipo_pagamento",
                values="valor",
                aggfunc="sum",
                fill_value=0
            )
            .rename(columns={
                "E": "Entradas (R$)",
                "S": "Saídas (R$)"
            })
            .sort_index()
        )

        # cria saldo semanal
        tabela["Saldo (R$)"] = tabela["Entradas (R$)"] + tabela["Saídas (R$)"]

        # formata valores
        tabela = tabela.applymap(lambda x: f"{x:,.2f}")

        # converte para markdown
        markdown = tabela.reset_index().rename(
            columns={"week_of_year": "Semana"}
        ).to_markdown(index=False)

        return (
            f"### 📊 Fluxo de caixa projetado — "
            f"{kwargs['mes']:02d}/{kwargs['ano']}\n\n"
            f"{markdown}"
        )