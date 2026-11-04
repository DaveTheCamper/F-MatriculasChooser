import math
import tkinter as tk

from rematriculador.model.dia_semana import DiaSemana

ALTURA_CABECALHO = 28
LARGURA_COLUNA_HORAS = 48
PRIMEIRA_HORA_PADRAO = 8
ULTIMA_HORA_PADRAO = 22
MARGEM_BLOCO = 2
CORES = ["#BBDEFB", "#C8E6C9", "#FFE0B2", "#E1BEE7", "#FFCDD2", "#B2EBF2", "#FFF9C4", "#D7CCC8", "#C5CAE9"]


class QuadroSemanal(tk.Canvas):
    def __init__(self, janela_pai):
        super().__init__(janela_pai, background="white", highlightthickness=1, highlightbackground="#B0B0B0")
        self.__aulas = []
        self.bind("<Configure>", lambda _: self.__desenhar())

    def exibir(self, grade):
        self.__aulas = grade.aulas() if grade else []
        self.__desenhar()

    def __desenhar(self):
        self.delete("all")
        self.__definir_escala()
        self.__desenhar_cabecalho()
        self.__desenhar_linhas_das_horas()
        self.__desenhar_aulas()

    def __definir_escala(self):
        inicios = [aula.horario.inicio.em_horas() for aula in self.__aulas]
        terminos = [aula.horario.termino.em_horas() for aula in self.__aulas]
        self.__primeira_hora = math.floor(min([PRIMEIRA_HORA_PADRAO, *inicios]))
        self.__ultima_hora = math.ceil(max([ULTIMA_HORA_PADRAO, *terminos]))
        quantidade_horas = self.__ultima_hora - self.__primeira_hora
        self.__altura_hora = (self.winfo_height() - ALTURA_CABECALHO - 2) / quantidade_horas
        self.__largura_dia = (self.winfo_width() - LARGURA_COLUNA_HORAS - 2) / len(DiaSemana)

    def __desenhar_cabecalho(self):
        for dia in DiaSemana:
            esquerda = self.__esquerda_do_dia(dia)
            self.create_line(esquerda, 0, esquerda, self.winfo_height(), fill="#D0D0D0")
            self.create_text(
                esquerda + self.__largura_dia / 2,
                ALTURA_CABECALHO / 2,
                text=dia.rotulo,
                font=("Segoe UI", 9, "bold"),
            )

    def __desenhar_linhas_das_horas(self):
        for hora in range(self.__primeira_hora, self.__ultima_hora):
            topo = self.__posicao_vertical(hora)
            self.create_line(0, topo, self.winfo_width(), topo, fill="#E4E4E4")
            self.create_text(6, topo + 2, anchor="nw", text=f"{hora:02d}:00", font=("Segoe UI", 8), fill="#606060")

    def __desenhar_aulas(self):
        codigos = sorted({aula.codigo_disciplina for aula in self.__aulas})
        for aula in self.__aulas:
            cor = CORES[codigos.index(aula.codigo_disciplina) % len(CORES)]
            self.__desenhar_aula(aula, cor)

    def __desenhar_aula(self, aula, cor):
        esquerda = self.__esquerda_do_dia(aula.horario.dia) + MARGEM_BLOCO
        direita = esquerda + self.__largura_dia - 2 * MARGEM_BLOCO
        topo = self.__posicao_vertical(aula.horario.inicio.em_horas())
        base = self.__posicao_vertical(aula.horario.termino.em_horas())
        self.create_rectangle(esquerda, topo, direita, base, fill=cor, outline="#707070")
        self.create_text(
            esquerda + 4,
            topo + 3,
            anchor="nw",
            width=direita - esquerda - 8,
            font=("Segoe UI", 8),
            text=f"{aula.nome_disciplina}\n{aula.turma.identificacao}\n{aula.horario.inicio}-{aula.horario.termino}",
        )

    def __esquerda_do_dia(self, dia):
        return LARGURA_COLUNA_HORAS + (dia.ordem - 1) * self.__largura_dia

    def __posicao_vertical(self, hora):
        return ALTURA_CABECALHO + (hora - self.__primeira_hora) * self.__altura_hora
