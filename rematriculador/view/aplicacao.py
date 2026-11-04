import tkinter as tk
from tkinter import messagebox, ttk

from rematriculador.model.excecoes import ErroRematriculador
from rematriculador.view.aba_disciplinas import AbaDisciplinas
from rematriculador.view.aba_grades import AbaGrades
from rematriculador.view.aba_preferencias import AbaPreferencias


class Aplicacao(tk.Tk):
    def __init__(self, servico):
        super().__init__()
        self.__servico = servico
        self.title("Rematriculador - Planejador de Rematrícula")
        self.geometry("1180x680")
        self.minsize(960, 560)
        self.__criar_menu()
        self.__criar_abas()

    def __criar_menu(self):
        barra = tk.Menu(self)
        arquivo = tk.Menu(barra, tearoff=False)
        arquivo.add_command(label="Carregar dados de exemplo", command=self.__carregar_exemplo)
        arquivo.add_separator()
        arquivo.add_command(label="Sair", command=self.destroy)
        barra.add_cascade(label="Arquivo", menu=arquivo)
        self.config(menu=barra)

    def __criar_abas(self):
        self.__caderno = ttk.Notebook(self)
        self.__caderno.pack(fill="both", expand=True, padx=8, pady=8)
        self.__abas = [
            (AbaDisciplinas(self.__caderno, self.__servico), "Disciplinas e turmas"),
            (AbaPreferencias(self.__caderno, self.__servico), "Preferências"),
            (AbaGrades(self.__caderno, self.__servico), "Grades"),
        ]
        for aba, titulo in self.__abas:
            self.__caderno.add(aba, text=titulo)
        self.__caderno.bind("<<NotebookTabChanged>>", lambda _: self.__atualizar_aba_atual())

    def __atualizar_aba_atual(self):
        aba, _ = self.__abas[self.__caderno.index("current")]
        aba.atualizar()

    def __carregar_exemplo(self):
        if not messagebox.askyesno("Exemplo", "Substituir os dados atuais pelos dados de exemplo?", parent=self):
            return
        try:
            self.__servico.carregar_exemplo()
        except ErroRematriculador as erro:
            messagebox.showerror("Erro", str(erro), parent=self)
        self.__atualizar_aba_atual()
