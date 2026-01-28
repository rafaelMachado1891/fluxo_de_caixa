from metricas.base import Metrica
from metrics import calcular_variacoes_saidas_entradas_saldo_operacional
from models.schema import ResultadoMetrica


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
        "melhora"
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

        if not registros:
            return ResultadoMetrica(
                metrica=self.nome,
                valor=None,
                status="sem_dados",
                ano=kwargs.get("ano"),
                mes=kwargs.get("mes"),
                unidade="BRL",
                tipo=self.fluxo,
                dominio=self.dominio,
                detalhes=None
            )

        dados = registros[0]  # ✅ sempre dict

        return ResultadoMetrica(
            metrica=self.nome,
            valor=None,
            status="ok",
            ano=kwargs.get("ano"),
            mes=kwargs.get("mes"),
            unidade="BRL",
            tipo=self.fluxo,
            dominio=self.dominio,
            detalhes={
                "entradas": dados.get("entradas"),
                "entradas_mes_anterior": dados.get("entradas_mes_anterior"),
                "variacao_entradas": dados.get("variacoes_entradas"),
                "saidas": dados.get("saidas"),
                "saidas_mes_anterior": dados.get("saidas_mes_anterior"),
                "variacao_saidas": dados.get("variacoes_saidas"),
                "saldo_operacional": dados.get("saldo_operacional"),
                "saldo_operacional_mes_anterior": dados.get("saldo_operacional_mes_anterior"),
                "variacao_saldo_operacional": dados.get("variacao_saldo_operacional"),
            }
        )