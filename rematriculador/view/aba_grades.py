import tkinter as tk
from tkinter import ttk

from rematriculador.view.aba_base import AbaBase
from rematriculador.view.painel_lista import PainelLista
from rematriculador.view.quadro_semanal import QuadroSemanal

LIMITE_EXIBICAO = 100
MENSAGEM_SEM_GRADES = (
    "Nenhuma grade válida. Cadastre turmas com horários ou reduza o mínimo de disciplinas nas preferências."
)


class AbaGrades(AbaBase):
    def __init__(self, janela_pai, servico):
        super().__init__(janela_pai, servico)
        self.__resumo = tk.StringVar()
        self.__detalhes = tk.StringVar()
        self.__rotulos = {}
        self.__lista = PainelLista(
            self, "Grades geradas", [("Opção", 80), ("Pontuação", 70), ("Disciplinas", 200)], []
        )
        self.__quadro = QuadroSemanal(self)
        self.__organizar_componentes()
        self.__lista.vincular_selecao(self.__exibir_selecionada)

    def atualizar(self):
        grades = self._servico.gerar_grades()
        exibidas = grades[:LIMITE_EXIBICAO]
        self.__rotulos = {
            id(item): self.__rotulo_da_opcao(posicao) for posicao, item in enumerate(exibidas)
        }
        self.__lista.preencher(exibidas, self.__valores_da_linha)
        self.__lista.selecionar_primeiro()
        self.__resumo.set(self.__texto_do_resumo(grades, exibidas))
        self.__quadro.exibir(None)
        self.__detalhes.set("")

    def __organizar_componentes(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        ttk.Label(self, textvariable=self.__resumo).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))
        self.__lista.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        self.__quadro.grid(row=1, column=1, sticky="nsew")
        ttk.Label(self, textvariable=self.__detalhes).grid(row=2, column=1, sticky="w", pady=(6, 0))

    def __rotulo_da_opcao(self, posicao):
        if posicao == 0:
            return "Principal"
        return f"Reserva {posicao}"

    def __valores_da_linha(self, item):
        codigos = ", ".join(turma.disciplina.codigo for turma in item.grade.turmas)
        return self.__rotulos[id(item)], f"{item.pontuacao_total:.1f}", codigos

    def __texto_do_resumo(self, grades, exibidas):
        if not grades:
            return MENSAGEM_SEM_GRADES
        return f"{len(grades)} grades válidas encontradas. Exibindo as {len(exibidas)} melhores."

    def __exibir_selecionada(self):
        item = self.__lista.item_selecionado()
        if item is None:
            return
        self.__quadro.exibir(item.grade)
        partes = [f"{pontos.nome_criterio}: {pontos.pontuacao:.1f}" for pontos in item.pontuacoes]
        self.__detalhes.set(" | ".join(partes))
