from dataclasses import dataclass

from rematriculador.model.distribuicao_dias import DistribuicaoDias
from rematriculador.model.excecoes import ErroDadosInvalidos


@dataclass(frozen=True)
class PreferenciasAluno:
    turnos_preferidos: frozenset = frozenset()
    distribuicao: DistribuicaoDias = DistribuicaoDias.EQUILIBRADA
    quantidade_minima_disciplinas: int = 1

    def __post_init__(self):
        if self.quantidade_minima_disciplinas < 1:
            raise ErroDadosInvalidos("A grade deve ter pelo menos uma disciplina.")
