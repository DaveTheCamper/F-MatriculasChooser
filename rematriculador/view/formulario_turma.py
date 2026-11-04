import tkinter as tk
from tkinter import ttk

from rematriculador.view.formulario_base import FormularioBase


class FormularioTurma(FormularioBase):
    def __init__(self, janela_pai, ao_confirmar, turma=None):
        self.__identificacao = tk.StringVar(value=turma.identificacao if turma else "")
        super().__init__(janela_pai, "Turma", ao_confirmar)

    def body(self, master):
        ttk.Label(master, text="Identificação:").grid(row=0, column=0, sticky="w", pady=2)
        campo = ttk.Entry(master, textvariable=self.__identificacao, width=30)
        campo.grid(row=0, column=1, pady=2)
        return campo

    def _valores(self):
        return (self.__identificacao.get(),)
