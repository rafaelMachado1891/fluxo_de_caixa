from pydantic import BaseModel
from typing import Optional, Literal, Dict, Any
from decimal import Decimal


# =========================
# REQUEST
# =========================

class PerguntaRequest(BaseModel):
    pergunta: str
    contexto: Optional[Dict[str, Any]] = None


# =========================
# RESULTADO DA MÉTRICA
# =========================

class ResultadoMetrica(BaseModel):
    metrica: str
    valor: Optional[Decimal]
    ano: Optional[int] = None
    mes: Optional[int] = None
    unidade: Optional[str] = None
    tipo: Optional[str] = None
    dominio: Optional[str] = None
    detalhes: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


# =========================
# DADOS DA RESPOSTA
# =========================

class ApiData(BaseModel):
    resultado: ResultadoMetrica
    visualizacao: Literal["texto", "tabela", "grafico", "alerta"]


# =========================
# METADADOS
# =========================

class ApiMeta(BaseModel):
    tempo_execucao: float
    fonte: str = "motor_analitico_v1"


# =========================
# RESPOSTA FINAL DA API
# =========================

class ApiResponse(BaseModel):
    success: bool
    status: Literal["ok", "sem_dados", "erro"]
    message: str
    data: Optional[ApiData]
    meta: ApiMeta