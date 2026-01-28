from fastapi import FastAPI, HTTPException
from models.schema import PerguntaRequest, ApiResponse
from agentes.agente import responder_usuario

app = FastAPI()


@app.post("/perguntar", response_model=ApiResponse)
def perguntar(req: PerguntaRequest):
    try:
        resposta = responder_usuario(
            pergunta=req.pergunta,
            contexto=req.contexto
        )

        # Garantia de contrato
        return ApiResponse(**resposta)

    except Exception as e:
        # Logue o erro se quiser
        print("Erro interno:", str(e))

        return ApiResponse(
            success=False,
            message="Erro interno ao processar a solicitação.",
            data=None,
            meta={
                "tempo_execucao": 0,
                "fonte": "motor_analitico_v1"
            }
        )
