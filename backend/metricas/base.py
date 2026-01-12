from abc import ABC, abstractmethod

class Metrica(ABC):
    parametros: dict = {}

    def normalizar_parametros(self, **kwargs):
        return kwargs

    @abstractmethod
    def executar(self, **kwargs):
        pass

    @abstractmethod
    def responder(self, resultado, **kwargs) -> str:
        pass