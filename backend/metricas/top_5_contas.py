from metricas.base import Metrica
from metrics import top_5_contas_saidas

class Top5ContasSaidas(Metrica):
    nome = "top_5_contas_saidas"
    parametros = ["ano", "mes"]

    def executar(self, **kwargs):
        return top_5_contas_saidas(
            ano=kwargs["ano"],
            mes=kwargs["mes"]
        )

    def responder(self, resultado, **kwargs) -> str:
        if not resultado:
            return "Não encontrei saídas para esse período."

        linhas = [
            f"- {r['conta_contabil']}: R$ {r['valor_total']:,.2f}"
            for r in resultado
        ]

        return (
            f"As contas que mais impactaram o caixa em "
            f"{kwargs['mes']:02d}/{kwargs['ano']} foram:\n"
            + "\n".join(linhas)
        )