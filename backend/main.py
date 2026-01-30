from fastapi import FastAPI
from models.schema import PerguntaRequest, ApiResponse
from agentes.agente import responder_usuario

app = FastAPI()


@app.post("/perguntar", response_model=ApiResponse)
def perguntar(req: PerguntaRequest):
    # A API apenas delega.
    # Toda lógica e tratamento estão no agente.
    return responder_usuario(
        pergunta=req.pergunta,
        contexto=req.contexto
    )
