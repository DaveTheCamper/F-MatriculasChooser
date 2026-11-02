from rematriculador.criterio.criterio_distribuicao import CriterioDistribuicao
from rematriculador.criterio.criterio_prioridade import CriterioPrioridade
from rematriculador.criterio.criterio_turno import CriterioTurno

PESO_PRIORIDADE = 0.5
PESO_DISTRIBUICAO = 0.3
PESO_TURNO = 0.2


class FabricaCriterios:
    def criar(self, disciplinas, preferencias):
        soma_prioridades = sum(disciplina.prioridade for disciplina in disciplinas)
        return [
            CriterioPrioridade(soma_prioridades, PESO_PRIORIDADE),
            CriterioDistribuicao(preferencias.distribuicao, PESO_DISTRIBUICAO),
            CriterioTurno(preferencias.turnos_preferidos, PESO_TURNO),
        ]
