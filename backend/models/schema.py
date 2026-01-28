from pydantic import BaseModel
from typing import Optional, Literal, Dict, Any, List
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

class ApiMeta(BaseModel):
    tempo_execucao: float
    fonte: str = "motor_analitico_v1"


class ApiData(BaseModel):
    metrica: Optional[str]
    resultado: Optional[ResultadoMetrica]
    detalhes: Optional[dict[str, Any]]
    


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[ApiData]
    meta: ApiMeta