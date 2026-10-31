from abc import ABC, abstractmethod

from rematriculador.model.grade_pontuada import PontuacaoCriterio

PONTUACAO_MAXIMA = 100.0


class CriterioAvaliacao(ABC):
    def __init__(self, peso):
        self.__peso = peso

    @property
    @abstractmethod
    def nome(self):
        pass

    @abstractmethod
    def pontuar(self, grade):
        pass

    def avaliar(self, grade):
        return PontuacaoCriterio(self.nome, self.pontuar(grade) * self.__peso)
