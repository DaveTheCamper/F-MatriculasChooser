import tkinter as tk
from tkinter import ttk

from rematriculador.model.disciplina import PRIORIDADE_MAXIMA, PRIORIDADE_MINIMA
from rematriculador.view.formulario_base import FormularioBase


class FormularioDisciplina(FormularioBase):
    def __init__(self, janela_pai, ao_confirmar, disciplina=None):
        self.__nome = tk.StringVar(value=disciplina.nome if disciplina else "")
        self.__codigo = tk.StringVar(value=disciplina.codigo if disciplina else "")
        self.__prioridade = tk.IntVar(value=disciplina.prioridade if disciplina else 3)
        super().__init__(janela_pai, "Disciplina", ao_confirmar)

    def body(self, master):
        ttk.Label(master, text="Nome:").grid(row=0, column=0, sticky="w", pady=2)
        campo_nome = ttk.Entry(master, textvariable=self.__nome, width=40)
        campo_nome.grid(row=0, column=1, pady=2)
        ttk.Label(master, text="Código:").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Entry(master, textvariable=self.__codigo, width=40).grid(row=1, column=1, pady=2)
        ttk.Label(master, text="Prioridade (1 a 5):").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Spinbox(
            master,
            from_=PRIORIDADE_MINIMA,
            to=PRIORIDADE_MAXIMA,
            textvariable=self.__prioridade,
            state="readonly",
            width=5,
        ).grid(row=2, column=1, sticky="w", pady=2)
        return campo_nome

    def _valores(self):
        return self.__nome.get(), self.__codigo.get(), self.__prioridade.get()
