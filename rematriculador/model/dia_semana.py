from enum import Enum

from rematriculador.model.excecoes import ErroDadosInvalidos


class DiaSemana(Enum):
    SEGUNDA = (1, "Segunda")
    TERCA = (2, "Terça")
    QUARTA = (3, "Quarta")
    QUINTA = (4, "Quinta")
    SEXTA = (5, "Sexta")
    SABADO = (6, "Sábado")

    def __init__(self, ordem, rotulo):
        self.ordem = ordem
        self.rotulo = rotulo

    @classmethod
    def a_partir_de_rotulo(cls, rotulo):
        for dia in cls:
            if dia.rotulo == rotulo:
                return dia
        raise ErroDadosInvalidos("Selecione um dia da semana.")
