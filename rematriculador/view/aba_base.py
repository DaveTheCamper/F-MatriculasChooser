from abc import ABC, abstractmethod
from tkinter import ttk


class AbaBase(ttk.Frame, ABC):
    def __init__(self, janela_pai, servico):
        super().__init__(janela_pai, padding=10)
        self._servico = servico

    @abstractmethod
    def atualizar(self):
        pass
