import re
from dataclasses import dataclass

from rematriculador.model.excecoes import ErroDadosInvalidos

MINUTOS_POR_HORA = 60
HORAS_POR_DIA = 24
MINUTOS_POR_DIA = HORAS_POR_DIA * MINUTOS_POR_HORA
FORMATO_HORA = re.compile(r"(\d{1,2}):(\d{2})")


@dataclass(frozen=True, order=True)
class HoraDoDia:
    minutos_desde_meia_noite: int

    def __post_init__(self):
        if not 0 <= self.minutos_desde_meia_noite < MINUTOS_POR_DIA:
            raise ErroDadosInvalidos("A hora deve estar entre 00:00 e 23:59.")

    @classmethod
    def a_partir_de_texto(cls, texto):
        correspondencia = FORMATO_HORA.fullmatch(texto.strip())
        if correspondencia is None:
            raise ErroDadosInvalidos(f"Hora inválida: '{texto}'. Use o formato HH:MM.")
        horas, minutos = map(int, correspondencia.groups())
        if horas >= HORAS_POR_DIA or minutos >= MINUTOS_POR_HORA:
            raise ErroDadosInvalidos(f"Hora inválida: '{texto}'.")
        return cls(horas * MINUTOS_POR_HORA + minutos)

    def minutos_ate(self, outra_hora):
        return outra_hora.minutos_desde_meia_noite - self.minutos_desde_meia_noite

    def em_horas(self):
        return self.minutos_desde_meia_noite / MINUTOS_POR_HORA

    def __str__(self):
        horas, minutos = divmod(self.minutos_desde_meia_noite, MINUTOS_POR_HORA)
        return f"{horas:02d}:{minutos:02d}"
