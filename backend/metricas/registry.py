from metricas.base import Metrica
from metricas.entradas_saidas_projetadas import EntradasSaidasProjetadas


REGISTRY: dict[str, Metrica] = {}

def carregar_metricas():
    for cls in Metrica.__subclasses__():
        instancia = cls()
        REGISTRY[instancia.nome] = instancia