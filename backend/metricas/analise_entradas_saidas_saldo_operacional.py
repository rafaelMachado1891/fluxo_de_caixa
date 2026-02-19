from metricas.base import Metrica
from metrics import calcular_variacoes_saidas_entradas_saldo_operacional
from models.schema import ResultadoMetrica
import pandas as pd


class VariacoesMetricas(Metrica):
    nome = "análise de variação do fluxo de caixa"
    descricao = "Variação mensal de entradas, saídas e saldo operacional"
    dominio = "caixa"
    fluxo = None

    tags = [
        "queda", 
        "redução",
        "aumento",
        "variação",
        "relação",
        "piora",
        "melhora",
        "saidas",
        "entradas",
        "saldo operacional"
    ]

    parametros = {
        "ano": {"tipo": int},
        "mes": {"tipo": int}
    }

    def executar(self, **kwargs):

        registros = calcular_variacoes_saidas_entradas_saldo_operacional(
            ano=kwargs.get("ano"),
            mes=kwargs.get("mes")
        )

        df = pd.DataFrame(registros)

        if not registros:
            return ResultadoMetrica(
                metrica=self.nome,
                valor=None,
                ano=kwargs.get("ano"),
                mes=kwargs.get("mes"),
                unidade="BRL",
                tipo=self.fluxo,
                dominio=self.dominio,
                detalhes=None
            )

        ano_mes = df.loc[0, "ano_mes"]
        entradas = df.loc[0, "entradas"]
        entradas_mes_anterior = df.loc[0, "entradas_mes_anterior"]
        variacao_entradas = df.loc[0, "variacao_entradas"]

        saidas = df.loc[0, "saidas"]
        saidas_mes_anterior = df.loc[0, "saidas_mes_anterior"]
        variacao_saidas = df.loc[0, "variacao_saidas"]

        saldo_operacional = df.loc[0, "saldo_operacional"]
        saldo_operacional_mes_anterior = df.loc[0, "saldo_operacional_mes_anterior"]
        variacao_saldo_operacional = df.loc[0, "variacao_saldo_operacional"]  

        resumo = {
            "ano_mes": ano_mes,
            "entradas_atual": entradas,
            "entradas_base": entradas_mes_anterior,
            "variacao_entradas": variacao_entradas,

            "saidas_atual": saidas,
            "saidas_base": saidas_mes_anterior,
            "variacao_saidas": variacao_saidas,

            "saldo_atual": saldo_operacional,
            "saldo_base": saldo_operacional_mes_anterior,
            "variacao_saldo": variacao_saldo_operacional
        }

        tabela = df[[
                    "ano_mes",
                    "entradas",
                    "entradas_mes_anterior",
                    "variacao_entradas",
                    "saidas",
                    "saidas_mes_anterior",
                    "variacao_saidas",
                    "saldo_operacional",
                    "saldo_operacional_mes_anterior",
                    "variacao_saldo_operacional"
                ]].to_dict(orient="records")

        return ResultadoMetrica(
            metrica=self.nome,
            valor=variacao_saldo_operacional,
            ano=kwargs.get("ano"),
            mes=kwargs.get("mes"),
            unidade="BRL",
            tipo=self.fluxo,
            dominio=self.dominio,
            detalhes={
                "resumo": resumo,
                "tabela": tabela
            }
        )