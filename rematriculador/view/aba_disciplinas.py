from tkinter import messagebox

from rematriculador.model.excecoes import ErroRematriculador
from rematriculador.view.aba_base import AbaBase
from rematriculador.view.formulario_disciplina import FormularioDisciplina
from rematriculador.view.formulario_horario import FormularioHorario
from rematriculador.view.formulario_turma import FormularioTurma
from rematriculador.view.painel_lista import PainelLista


class AbaDisciplinas(AbaBase):
    def __init__(self, janela_pai, servico):
        super().__init__(janela_pai, servico)
        self.__painel_disciplinas = self.__criar_painel_disciplinas()
        self.__painel_turmas = self.__criar_painel_turmas()
        self.__painel_horarios = self.__criar_painel_horarios()
        self.__organizar_paineis()
        self.__painel_disciplinas.vincular_selecao(self.__atualizar_turmas)
        self.__painel_turmas.vincular_selecao(self.__atualizar_horarios)

    def atualizar(self):
        self.__painel_disciplinas.preencher(
            self._servico.disciplinas,
            lambda disciplina: (disciplina.codigo, disciplina.nome, disciplina.prioridade),
        )
        self.__atualizar_turmas()

    def __criar_painel_disciplinas(self):
        return PainelLista(
            self,
            "Disciplinas",
            [("Código", 70), ("Nome", 260), ("Prioridade", 70)],
            [
                ("Nova", self.__nova_disciplina),
                ("Editar", self.__editar_disciplina),
                ("Excluir", self.__excluir_disciplina),
            ],
        )

    def __criar_painel_turmas(self):
        return PainelLista(
            self,
            "Turmas da disciplina",
            [("Turma", 150), ("Horários", 50)],
            [
                ("Nova", self.__nova_turma),
                ("Editar", self.__editar_turma),
                ("Excluir", self.__excluir_turma),
            ],
        )

    def __criar_painel_horarios(self):
        return PainelLista(
            self,
            "Horários da turma",
            [("Dia", 70), ("Início", 55), ("Término", 55), ("Turno", 55)],
            [
                ("Novo", self.__novo_horario),
                ("Editar", self.__editar_horario),
                ("Excluir", self.__excluir_horario),
            ],
        )

    def __organizar_paineis(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.__painel_disciplinas.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        self.__painel_turmas.grid(row=0, column=1, sticky="nsew", padx=(0, 6))
        self.__painel_horarios.grid(row=0, column=2, sticky="nsew")

    def __atualizar_turmas(self):
        disciplina = self.__painel_disciplinas.item_selecionado()
        turmas = disciplina.turmas if disciplina else ()
        self.__painel_turmas.preencher(
            turmas, lambda turma: (turma.identificacao, len(turma.horarios))
        )
        self.__atualizar_horarios()

    def __atualizar_horarios(self):
        turma = self.__painel_turmas.item_selecionado()
        horarios = turma.horarios if turma else ()
        self.__painel_horarios.preencher(
            horarios,
            lambda horario: (
                horario.dia.rotulo,
                str(horario.inicio),
                str(horario.termino),
                horario.turno.rotulo,
            ),
        )

    def __nova_disciplina(self):
        FormularioDisciplina(self, self.__salvando(self._servico.cadastrar_disciplina))

    def __editar_disciplina(self):
        disciplina = self.__exigir(self.__painel_disciplinas, "uma disciplina")
        if disciplina is None:
            return
        salvar = lambda *valores: self._servico.editar_disciplina(disciplina.codigo, *valores)
        FormularioDisciplina(self, self.__salvando(salvar), disciplina)

    def __excluir_disciplina(self):
        disciplina = self.__exigir(self.__painel_disciplinas, "uma disciplina")
        if disciplina is None:
            return
        if messagebox.askyesno("Excluir", f"Excluir a disciplina {disciplina.nome}?", parent=self):
            self.__executar(lambda: self._servico.excluir_disciplina(disciplina.codigo))

    def __nova_turma(self):
        disciplina = self.__exigir(self.__painel_disciplinas, "uma disciplina")
        if disciplina is None:
            return
        salvar = lambda identificacao: self._servico.cadastrar_turma(disciplina.codigo, identificacao)
        FormularioTurma(self, self.__salvando(salvar))

    def __editar_turma(self):
        turma = self.__exigir(self.__painel_turmas, "uma turma")
        if turma is None:
            return
        salvar = lambda identificacao: self._servico.editar_turma(
            turma.disciplina.codigo, turma.identificacao, identificacao
        )
        FormularioTurma(self, self.__salvando(salvar), turma)

    def __excluir_turma(self):
        turma = self.__exigir(self.__painel_turmas, "uma turma")
        if turma is None:
            return
        if messagebox.askyesno("Excluir", f"Excluir a turma {turma.identificacao}?", parent=self):
            self.__executar(
                lambda: self._servico.excluir_turma(turma.disciplina.codigo, turma.identificacao)
            )

    def __novo_horario(self):
        turma = self.__exigir(self.__painel_turmas, "uma turma")
        if turma is None:
            return
        salvar = lambda *valores: self._servico.cadastrar_horario(turma, *valores)
        FormularioHorario(self, self.__salvando(salvar))

    def __editar_horario(self):
        turma = self.__exigir(self.__painel_turmas, "uma turma")
        horario = self.__exigir(self.__painel_horarios, "um horário")
        if turma is None or horario is None:
            return
        salvar = lambda *valores: self._servico.editar_horario(turma, horario, *valores)
        FormularioHorario(self, self.__salvando(salvar), horario)

    def __excluir_horario(self):
        turma = self.__exigir(self.__painel_turmas, "uma turma")
        horario = self.__exigir(self.__painel_horarios, "um horário")
        if turma is None or horario is None:
            return
        self.__executar(lambda: self._servico.excluir_horario(turma, horario))

    def __exigir(self, painel, descricao):
        item = painel.item_selecionado()
        if item is None:
            messagebox.showinfo("Seleção", f"Selecione {descricao} na lista.", parent=self)
        return item

    def __salvando(self, acao):
        def salvar_e_atualizar(*valores):
            acao(*valores)
            self.atualizar()

        return salvar_e_atualizar

    def __executar(self, acao):
        try:
            acao()
        except ErroRematriculador as erro:
            messagebox.showerror("Erro", str(erro), parent=self)
        self.atualizar()
