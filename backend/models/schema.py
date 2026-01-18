from pydantic import BaseModel
from typing import Optional, Literal, Dict, Any

class ResultadoMetrica(BaseModel):
    metrica: Optional[str]
    valor: Optional[float]

    status: Literal["ok","sem_dados", "erro"]
    ano: Optional[int] = None
    
    mes: Optional[int] = None
    unidade: Optional[str] = None
    tipo: Optional[str] = None
    dominio: Optional[str] = None
    detalhes: Optional[dict[Any,str]] = None

    class Config:
        from_attributes = True


class PerguntaRequest(BaseModel):
    pergunta: str
    contexto: dict | None = None


class RespostaResponse(BaseModel):
    resposta: str