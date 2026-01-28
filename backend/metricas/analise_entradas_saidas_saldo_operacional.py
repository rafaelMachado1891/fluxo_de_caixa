from metricas.base import Metrica
from metrics import calcular_variacoes_saidas_entradas_saldo_operacional
from models.schema import ResultadoMetrica


class VariacoesMetricas(Metrica):
    nome = "variacao_metricas_financeiras"
    descricao = "Variação mensal de entradas, saídas e saldo operacional"
    dominio = "caixa"
    fluxo = None

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

        # 🔥 pega o único registro retornado
        dados = registros[0]

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
                "entradas": dados["entradas"],
                "entradas_mes_anterior": dados["entradas_mes_anterior"],
                "variacao_entradas": dados["variacoes_entradas"],
                "saidas": dados["saidas"],
                "saidas_mes_anterior": dados["saidas_mes_anterior"],
                "variacao_saidas": dados["variacoes_saidas"],
                "saldo_operacional": dados["saldo_operacional"],
                "saldo_operacional_mes_anterior": dados["saldo_operacional_mes_anterior"],
                "variacao_saldo_operacional": dados["variacao_saldo_operacional"],
            }
        )