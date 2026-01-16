from metricas.base import Metrica
from metrics import calcular_cobertura_de_caixa

class CoberturaDeCaixa(Metrica):
    nome = "cobertura de caixa"
    descricao = "Calculo da Cobertura de caixa projetadaconsiderando o saldo atual de caixa"
    dominio = "caixa"
    fluxo = "projetado"
    tags = ["cobertura de caixa"]
    
    parametros = {}
    
    def executar(self, **kwargs):
        return calcular_cobertura_de_caixa()            
        
    def responder(self, resultado, **kwargs) -> str:
        cobertura = resultado

        if cobertura is None:
            return "⚠️ Não há dados suficientes para calcular a cobertura de caixa."

        return  (
            f"## 💼 Cobertura de Caixa\n\n"
            f"A cobertura de caixa calculada é de **{cobertura:.2f}** meses."
        )

        