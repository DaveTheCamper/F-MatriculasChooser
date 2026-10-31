from enum import Enum


class DistribuicaoDias(Enum):
    CONCENTRADA = "Concentrar as aulas em menos dias"
    EQUILIBRADA = "Distribuir as aulas ao longo da semana"

    @property
    def rotulo(self):
        return self.value
