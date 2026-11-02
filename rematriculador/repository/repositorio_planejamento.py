from abc import ABC, abstractmethod


class RepositorioPlanejamento(ABC):
    @abstractmethod
    def carregar(self):
        pass

    @abstractmethod
    def salvar(self, planejamento):
        pass
