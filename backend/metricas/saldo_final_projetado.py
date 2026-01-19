from metricas.base import Metrica
from metrics import calcular_saldo_final_projetado
from models.schema import ResultadoMetrica

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

    def executar(self, **kwargs) -> dict:
        saldo = calcular_saldo_final_projetado(
            ano=kwargs.get("ano"),
            mes=kwargs.get("mes")
        )

        return ResultadoMetrica(
            metrica=self.nome,
            valor=saldo,
            status="ok" if saldo is not None else "sem_dados",
            ano=kwargs.get("ano"),
            mes=kwargs.get("mes"),
            unidade="BRL",
            tipo=self.fluxo,
            dominio=self.dominio,
            detalhes=None
        )