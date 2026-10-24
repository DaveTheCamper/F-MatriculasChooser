from dataclasses import dataclass

from rematriculador.model.dia_semana import DiaSemana
from rematriculador.model.excecoes import ErroDadosInvalidos
from rematriculador.model.hora_do_dia import HoraDoDia
from rematriculador.model.turno import Turno


@dataclass(frozen=True)
class Horario:
    dia: DiaSemana
    inicio: HoraDoDia
    termino: HoraDoDia

    def __post_init__(self):
        if self.inicio >= self.termino:
            raise ErroDadosInvalidos("O término deve ser depois do início.")

    @property
    def turno(self):
        return Turno.da_hora(self.inicio)

    def se_sobrepoe(self, outro_horario):
        if self.dia != outro_horario.dia:
            return False
        return self.inicio < outro_horario.termino and outro_horario.inicio < self.termino

    def chave_de_ordenacao(self):
        return self.dia.ordem, self.inicio

    def __str__(self):
        return f"{self.dia.rotulo} {self.inicio}-{self.termino}"
