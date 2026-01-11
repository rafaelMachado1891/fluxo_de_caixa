from metrics import saldo_operacional_mes
from metricas.base import Metrica

class SaldoOperacionalMes(Metrica):
    nome = "saldo_operacional_mes"
    parametros = ["ano","mes"]
    descricao = "Saldo operacional de entradas menos saídas realizadas no mês"
    palavras_chave = ["saldo", "resultado", "fechamento", "operacional"]

    def executar(self, **kwargs):
        return saldo_operacional_mes(
            ano=kwargs["ano"],
            mes=kwargs["mes"]
        )
    
    def responder(self, resultado, **kwargs) -> str:
        return (
            f"O saldo operacional realizado em "
            f"{kwargs['mes']:02d}/{kwargs['ano']} "
            f"foi R$ {resultado:,.2f}."
        )