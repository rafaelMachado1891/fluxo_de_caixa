from abc import ABC, abstractmethod
from typing import Any, Dict

class Metrica(ABC):
    parametros: dict = {}

    def normalizar_parametros(self, **kwargs) -> dict:
        return kwargs

    @abstractmethod
    def executar(self, **kwargs) -> Dict[str, Any ]:
        
        
        pass
