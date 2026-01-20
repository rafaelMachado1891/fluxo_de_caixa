from pydantic import BaseModel
from typing import Optional, Literal, Dict, Any
from decimal import Decimal

class ResultadoMetrica(BaseModel):
    metrica: Optional[str]
    valor: Decimal | float | None

    status: Literal["ok","sem_dados", "erro"]
    ano: Optional[int] = None
    
    mes: Optional[int] = None
    unidade: Optional[str] = None
    tipo: Optional[str] = None
    dominio: Optional[str] = None
    detalhes: Optional[dict[str, Any]] = None

    class Config:
        from_attributes = True


class PerguntaRequest(BaseModel):
    pergunta: str
    contexto: Optional[Dict[str, Any]] = None


class RespostaResponse(BaseModel):
    resposta: str

    class Config:
        from_attributes = True