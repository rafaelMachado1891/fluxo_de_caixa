from metricas.base import Metrica
from metricas.entradas_saidas_projetadas import EntradasSaidasProjetadas
from metricas.saldo_operacional_projetado import SaldoOperacionalProjetado
from metricas.saldo_final_projetado import SaldoFinalProjetado


REGISTRY: dict[str, Metrica] = {}

def carregar_metricas():
    for cls in Metrica.__subclasses__():
        instancia = cls()
        REGISTRY[instancia.nome] = instancia