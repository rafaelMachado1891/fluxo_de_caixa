from metrics import saldo_operacional_projetado_negativo
from metricas.base import Metrica
import pandas as pd
import tabulate

class SaldoOperacionalNegativo(Metrica):
    nome = "semanas com pressão sobre o caixa projetado"
    descricao = "lista de semanas com saldo operacional projetado negativo"
    
    parametros = ["ano","mes"]
    dominio = "caixa"

    def executar(self, **kwargs):
        return saldo_operacional_projetado_negativo(
            ano=kwargs["ano"],
            mes=kwargs["mes"]
        )
    
    def responder(self, resultado, **kwargs) -> str: 
        # cria DataFrame 
        df = pd.DataFrame(resultado) 
        
        df["week_of_year"] = df["week_of_year"].astype(int) 
        df["ano_mes"] = df["ano_mes"].astype(str) 
        df["saldo_operacional"] = df["saldo_operacional"].astype(float) 
        
        df["saldo_operacional"] = df["saldo_operacional"].apply(lambda x: f"{x:,.2f}") 
        
        markdown = df.rename(
             columns={ 
                 "ano_mes": "Ano/Mês",
                 "week_of_year": "Semana",
                 "saldo_operacional": "Saldo Operacional" 
                 } ).to_markdown(index=False)
        
        return ( f"### 📊 Semanas com pressão de caixa — "
                 f"{kwargs['mes']:02d}/{kwargs['ano']}\n\n" 
                 f"{markdown}" 
                 )