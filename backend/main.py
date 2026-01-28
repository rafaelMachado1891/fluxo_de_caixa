from fastapi import FastAPI
from models.schema import PerguntaRequest, ApiResponse
from agentes.agente import responder_usuario

app = FastAPI()


@app.post("/perguntar", response_model=ApiResponse)
def perguntar(req: PerguntaRequest):
    try:
        return responder_usuario(
            pergunta=req.pergunta,
            contexto=req.contexto
        )
    except Exception as e:
        return {
            "success": False,
            "message": "Erro interno ao processar a solicitação.",
            "data": None,
            "meta": {
                "tempo_execucao": 0,
                "fonte": "motor_analitico_v1"
            }
        }
