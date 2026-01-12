from metricas.base import Metrica
from metricas.saldo_operacional_mes import SaldoOperacionalMes
from metricas.top_5_contas import Top5ContasSaidas
from metricas.entradas_saidas_projetadas import EntradasSaidasProjetadas
from metricas.semanas_com_pior_saldo_operacional import SaldoOperacionalNegativo

REGISTRY: dict[str, Metrica] = {}

def carregar_metricas():
    for cls in Metrica.__subclasses__():
        instancia = cls()
        REGISTRY[instancia.nome] = instancia