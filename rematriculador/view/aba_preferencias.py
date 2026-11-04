import tkinter as tk
from tkinter import messagebox, ttk

from rematriculador.model.distribuicao_dias import DistribuicaoDias
from rematriculador.model.excecoes import ErroRematriculador
from rematriculador.model.preferencias_aluno import PreferenciasAluno
from rematriculador.model.turno import Turno
from rematriculador.view.aba_base import AbaBase

QUANTIDADE_MAXIMA_NO_SELETOR = 15


class AbaPreferencias(AbaBase):
    def __init__(self, janela_pai, servico):
        super().__init__(janela_pai, servico)
        self.__turnos = {turno: tk.BooleanVar() for turno in Turno}
        self.__distribuicao = tk.StringVar()
        self.__quantidade_minima = tk.IntVar()
        self.__mensagem = tk.StringVar()
        self.__criar_secao_turnos()
        self.__criar_secao_distribuicao()
        self.__criar_secao_quantidade()
        self.__criar_rodape()

    def atualizar(self):
        preferencias = self._servico.preferencias
        for turno, variavel in self.__turnos.items():
            variavel.set(turno in preferencias.turnos_preferidos)
        self.__distribuicao.set(preferencias.distribuicao.name)
        self.__quantidade_minima.set(preferencias.quantidade_minima_disciplinas)
        self.__mensagem.set("")

    def __criar_secao_turnos(self):
        secao = ttk.LabelFrame(self, text="Turnos preferidos", padding=8)
        secao.pack(fill="x", pady=(0, 8))
        for turno, variavel in self.__turnos.items():
            ttk.Checkbutton(secao, text=turno.rotulo, variable=variavel).pack(side="left", padx=(0, 12))

    def __criar_secao_distribuicao(self):
        secao = ttk.LabelFrame(self, text="Distribuição dos dias", padding=8)
        secao.pack(fill="x", pady=(0, 8))
        for distribuicao in DistribuicaoDias:
            ttk.Radiobutton(
                secao,
                text=distribuicao.rotulo,
                value=distribuicao.name,
                variable=self.__distribuicao,
            ).pack(anchor="w")

    def __criar_secao_quantidade(self):
        secao = ttk.LabelFrame(self, text="Quantidade de disciplinas", padding=8)
        secao.pack(fill="x", pady=(0, 8))
        ttk.Label(secao, text="Mínimo de disciplinas por grade:").pack(side="left", padx=(0, 8))
        ttk.Spinbox(
            secao,
            from_=1,
            to=QUANTIDADE_MAXIMA_NO_SELETOR,
            textvariable=self.__quantidade_minima,
            state="readonly",
            width=5,
        ).pack(side="left")

    def __criar_rodape(self):
        rodape = ttk.Frame(self)
        rodape.pack(fill="x")
        ttk.Button(rodape, text="Salvar preferências", command=self.__salvar).pack(side="left")
        ttk.Label(rodape, textvariable=self.__mensagem).pack(side="left", padx=8)

    def __salvar(self):
        turnos = frozenset(turno for turno, variavel in self.__turnos.items() if variavel.get())
        try:
            self._servico.atualizar_preferencias(
                PreferenciasAluno(
                    turnos,
                    DistribuicaoDias[self.__distribuicao.get()],
                    self.__quantidade_minima.get(),
                )
            )
        except ErroRematriculador as erro:
            messagebox.showerror("Erro", str(erro), parent=self)
            return
        self.__mensagem.set("Preferências salvas.")
