from models.schema import ResultadoMetrica

def decidir_visualizacao(resultado: ResultadoMetrica) -> str:
    if resultado.detalhes is None:
        return "texto"

    if isinstance(resultado.detalhes, dict):
        if "tabela" in resultado.detalhes:
            return "tabela"

    return "texto"