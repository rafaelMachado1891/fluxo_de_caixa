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
        
        resposta = calcular_cobertura_de_caixa()
        
        return {
            "metrica": self.nome,
            "valor": resposta,
            "status": "ok" if resposta is not None else "sem_dados",
            "ano": None,
            "mes": None,
            "unidade": "BRL",
            "tipo": self.fluxo,
            "dominio": self.dominio,
            "detalhes": None
        }

        