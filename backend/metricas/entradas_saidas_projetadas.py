from metricas.base import Metrica
from metrics import calcular_total_entradas_saidas_por_mes
import pandas as pd
from models.schema import ResultadoMetrica


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

    def executar(self, **kwargs) -> ResultadoMetrica:
        registros = calcular_total_entradas_saidas_por_mes(
            ano=kwargs.get("ano"),
            mes=kwargs.get("mes")
        )

        df = pd.DataFrame(registros)

        # Caso não tenha dados
        if df.empty:
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

        # Agregações principais
        saldo_total = float(df["saldo_operacional"].sum())
        entradas_total = float(df["entradas"].sum())
        saidas_total = float(df["saidas"].sum())

        return ResultadoMetrica(
            metrica=self.nome,
            valor=saldo_total,
            ano=kwargs.get("ano"),
            mes=kwargs.get("mes"),
            unidade="BRL",
            tipo=self.fluxo,
            dominio=self.dominio,
            detalhes={
                "resumo": {
                    "entradas_total": entradas_total,
                    "saidas_total": saidas_total,
                    "saldo_total": saldo_total
                },
                "tabela": df.to_dict(orient="records")
            }
        )
