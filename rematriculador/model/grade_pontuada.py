from dataclasses import dataclass

from rematriculador.model.grade_horaria import GradeHoraria


@dataclass(frozen=True)
class PontuacaoCriterio:
    nome_criterio: str
    pontuacao: float


@dataclass(frozen=True)
class GradePontuada:
    grade: GradeHoraria
    pontuacoes: tuple

    @property
    def pontuacao_total(self):
        return sum(item.pontuacao for item in self.pontuacoes)
