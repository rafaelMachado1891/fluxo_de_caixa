from metricas.base import Metrica
import pandas as pd
from metrics import calcular_saldo_operacional_projetado
from models.schema import ResultadoMetrica


class SaldoOperacionalProjetado(Metrica):
        nome = "saldo operacional projetado"
        descricao = "Saldo operacional projetado para o mês"
        dominio = "caixa"
        fluxo = "projetado"

        tags = [
            "saldo operacional",
            "projetado",
            "mensal"
        ]

        parametros = {
            "ano": {"tipo": int},
            "mes": {"tipo": int}
        }

        def executar(self, **kwargs):
            saldo = calcular_saldo_operacional_projetado(
                ano=kwargs.get("ano"),
                mes=kwargs.get("mes")
            )
            
            return ResultadoMetrica(
                metrica = self.nome,
                valor = saldo,
                ano = kwargs.get("ano"),
                mes = kwargs.get("mes"),
                unidade = "BRL",
                tipo = self.fluxo,
                dominio = self.dominio,
                detalhes = None       
            )
            
        