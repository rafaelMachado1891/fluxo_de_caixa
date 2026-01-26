from fastapi import FastAPI
from models.schema import PerguntaRequest, ApiResponse
from agentes.agente import responder_usuario

app = FastAPI()


@app.post("/perguntar", response_model=ApiResponse)
def perguntar(req: PerguntaRequest):
    resposta = responder_usuario(
        pergunta=req.pergunta,
        contexto=req.contexto
    )
    return resposta
