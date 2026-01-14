from metricas.base import Metrica
from metrics import calcular_saldo_final_projetado

class SaldoFinalProjetado(Metrica):
    nome = "saldo final projetado"
    descricao = "Saldo final projetado para o mês"
    dominio = "caixa"
    fluxo = "projetado"

    tags = [
        "saldo final",
        "projetado",
        "mensal"
    ]

    parametros = {
        "ano": {"tipo": int},
        "mes": {"tipo": int}
    }

    def executar(self, **kwargs):
        return calcular_saldo_final_projetado(
            ano=kwargs.get("ano"),
            mes=kwargs.get("mes")
        )

    def responder(self, resultado, **kwargs) -> str:
        saldo = resultado

        if saldo is None:
            return "⚠️ Não há dados projetados para o período informado."

        mes = kwargs.get("mes", "mês atual")
        ano = kwargs.get("ano", "ano atual")

        resposta = (
            f"## 💼 Saldo Final Projetado\n"
            f"📅 **Período:** {mes}/{ano}\n\n"
            f"O saldo final projetado para o período é de **R$ {saldo:,.2f}**."
        )

        return resposta