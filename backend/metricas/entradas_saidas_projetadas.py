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

    def executar(self, **kwargs) -> dict:
        registros = calcular_total_entradas_saidas_por_mes(
        ano=kwargs.get("ano"),
        mes=kwargs.get("mes")
    )

        df = pd.DataFrame(registros)

        if df.empty:
            return {
                "metrica": self.nome,
                "valor": None,
                "status": "sem_dados",
                "ano": kwargs.get("ano"),
                "mes": kwargs.get("mes"),
                "unidade": "BRL",
                "tipo": self.fluxo,
                "dominio": self.dominio,
                "detalhes": None
            }

        saldo_total = df["saldo_operacional"].sum()
        entradas_total = df["entradas"].sum()
        saidas_total = df["saidas"].sum()

        return ResultadoMetrica(
            metrica=self.nome,
            valor=saldo_total,
            status="ok",
            ano=kwargs.get("ano"),
            mes=kwargs.get("mes"),
            unidade="BRL",
            tipo=self.fluxo,
            dominio=self.dominio,
            detalhes={
                "entradas_total": entradas_total,
                "saidas_total": saidas_total,
                "por_semana": df.to_dict(orient="records")
            }
        )