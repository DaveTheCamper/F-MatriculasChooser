import tkinter as tk
from tkinter import ttk

from rematriculador.model.dia_semana import DiaSemana
from rematriculador.view.formulario_base import FormularioBase


class FormularioHorario(FormularioBase):
    def __init__(self, janela_pai, ao_confirmar, horario=None):
        self.__dia = tk.StringVar(value=horario.dia.rotulo if horario else DiaSemana.SEGUNDA.rotulo)
        self.__inicio = tk.StringVar(value=str(horario.inicio) if horario else "19:00")
        self.__termino = tk.StringVar(value=str(horario.termino) if horario else "22:00")
        super().__init__(janela_pai, "Horário", ao_confirmar)

    def body(self, master):
        ttk.Label(master, text="Dia:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Combobox(
            master,
            textvariable=self.__dia,
            values=[dia.rotulo for dia in DiaSemana],
            state="readonly",
            width=12,
        ).grid(row=0, column=1, sticky="w", pady=2)
        ttk.Label(master, text="Início (HH:MM):").grid(row=1, column=0, sticky="w", pady=2)
        campo_inicio = ttk.Entry(master, textvariable=self.__inicio, width=14)
        campo_inicio.grid(row=1, column=1, sticky="w", pady=2)
        ttk.Label(master, text="Término (HH:MM):").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Entry(master, textvariable=self.__termino, width=14).grid(row=2, column=1, sticky="w", pady=2)
        return campo_inicio

    def _valores(self):
        return self.__dia.get(), self.__inicio.get(), self.__termino.get()
