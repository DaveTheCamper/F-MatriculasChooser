from enum import Enum

from rematriculador.model.hora_do_dia import HoraDoDia, MINUTOS_POR_HORA

INICIO_DA_TARDE = HoraDoDia(12 * MINUTOS_POR_HORA)
INICIO_DA_NOITE = HoraDoDia(18 * MINUTOS_POR_HORA)


class Turno(Enum):
    MANHA = "Manhã"
    TARDE = "Tarde"
    NOITE = "Noite"

    @property
    def rotulo(self):
        return self.value

    @classmethod
    def da_hora(cls, hora):
        if hora < INICIO_DA_TARDE:
            return cls.MANHA
        if hora < INICIO_DA_NOITE:
            return cls.TARDE
        return cls.NOITE
