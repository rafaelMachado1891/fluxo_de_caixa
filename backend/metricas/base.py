from abc import ABC, abstractmethod

class Metrica(ABC): 
    nome: str
    parametros: list[str]
    descricao: str = ""
    palavras_chave: list[str] = []

    @abstractmethod
    def executar(self, **kwargs):
        pass

    @abstractmethod
    def responder(self, resultado, **kwargs) -> str:
        pass
