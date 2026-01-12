from abc import ABC, abstractmethod
from typing import List

class Metrica(ABC):
    nome: str
    descricao: str = ""
    dominio: str = ""
    fluxo: str = ""
    tags: List[str] = []

    parametros: List[str] = []           # aceitos
    parametros_obrigatorios: List[str] = []  # obrigatórios

    def validar_parametros(self, **kwargs):
        for p in self.parametros_obrigatorios:
            if kwargs.get(p) is None:
                raise ValueError(
                    f"⚠️ Parâmetro '{p}' ausente para a métrica '{self.nome}'."
                )

    @abstractmethod
    def executar(self, **kwargs):
        pass

    @abstractmethod
    def responder(self, resultado, **kwargs) -> str:
        pass
