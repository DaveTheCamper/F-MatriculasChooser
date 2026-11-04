from abc import ABC, abstractmethod
from tkinter import messagebox, simpledialog, ttk

from rematriculador.model.excecoes import ErroRematriculador


class FormularioBase(simpledialog.Dialog, ABC):
    def __init__(self, janela_pai, titulo, ao_confirmar):
        self.__ao_confirmar = ao_confirmar
        super().__init__(janela_pai, titulo)

    def buttonbox(self):
        barra = ttk.Frame(self)
        barra.pack(pady=8)
        ttk.Button(barra, text="Confirmar", command=self.ok).pack(side="left", padx=4)
        ttk.Button(barra, text="Cancelar", command=self.cancel).pack(side="left", padx=4)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def validate(self):
        try:
            self.__ao_confirmar(*self._valores())
        except ErroRematriculador as erro:
            messagebox.showerror("Dados inválidos", str(erro), parent=self)
            return False
        return True

    @abstractmethod
    def _valores(self):
        pass
