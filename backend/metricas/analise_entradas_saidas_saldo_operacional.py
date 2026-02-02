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

        entradas = df["entradas"]
        entradas_mes_anterior = df['entradas_mes_anterior']
        variacao_entradas = df["variacao_entradas"]

        saidas = df["saidas"]
        saidas_mes_anterior = df["saidas_mes_anterior"]
        variacao_saidas = df["variacao_saidas"]

        saldo_operacional = df["saldo_operacional"]
        saldo_operacional_mes_anterior = df["saldo_operacional_mes_anterior"]
        variacao_saldo_operacional = df["variacao_saldo_operacional"]


        

        return ResultadoMetrica(
            metrica=self.nome,
            valor=None,
            ano=kwargs.get("ano"),
            mes=kwargs.get("mes"),
            unidade="BRL",
            tipo=self.fluxo,
            dominio=self.dominio,
            detalhes={
                "entradas": entradas,
                "entradas_mes_anterior": entradas_mes_anterior,
                "variacao_entradas": variacao_entradas,
                "saidas": saidas,
                "saidas_mes_anterior": saidas_mes_anterior,
                "variacao_saidas": variacao_saidas,
                "saldo_operacional": saldo_operacional,
                "saldo_operacional_mes_anterior": saldo_operacional_mes_anterior,
                "variacao_saldo_operacional": variacao_saldo_operacional,
            }
        )