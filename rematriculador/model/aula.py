from dataclasses import dataclass

from rematriculador.model.horario import Horario
from rematriculador.model.turma import Turma


@dataclass(frozen=True)
class Aula:
    turma: Turma
    horario: Horario

    @property
    def nome_disciplina(self):
        return self.turma.disciplina.nome

    @property
    def codigo_disciplina(self):
        return self.turma.disciplina.codigo
