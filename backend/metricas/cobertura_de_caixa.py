from metricas.base import Metrica
from metrics import calcular_cobertura_de_caixa
from models.schema import ResultadoMetrica

class CoberturaDeCaixa(Metrica):
    nome = "cobertura de caixa"
    descricao = "Calculo quantos meses o caixa sustenta a operação."
    dominio = "caixa"
    fluxo = "projetado"
    tags = ["cobertura de caixa"]
    
    parametros = {}
    
    def executar(self, **kwargs):
        
        resposta = calcular_cobertura_de_caixa()
        
        return ResultadoMetrica(
            metrica =  self.nome,
            valor = resposta,
            ano = None,
            mes = None,
            unidade = "mes",
            tipo = self.fluxo,
            dominio = self.dominio,
            detalhes = None
        )



        