import unittest

from rematriculador.model.dia_semana import DiaSemana
from rematriculador.model.disciplina import Disciplina
from rematriculador.model.excecoes import (
    ErroDadosInvalidos,
    ErroRegistroDuplicado,
    ErroRegistroNaoEncontrado,
)
from tests.test_hora_e_horario import criar_horario


class TesteDisciplina(unittest.TestCase):
    def setUp(self):
        self.disciplina = Disciplina("Compiladores", "comp", 4)

    def test_normaliza_codigo(self):
        self.assertEqual(self.disciplina.codigo, "COMP")

    def test_rejeita_nome_vazio(self):
        with self.assertRaises(ErroDadosInvalidos):
            Disciplina("  ", "COMP", 3)

    def test_rejeita_prioridade_fora_da_faixa(self):
        with self.assertRaises(ErroDadosInvalidos):
            Disciplina("Compiladores", "COMP", 6)

    def test_rejeita_turma_repetida(self):
        self.disciplina.criar_turma("A")
        with self.assertRaises(ErroRegistroDuplicado):
            self.disciplina.criar_turma(" A ")

    def test_renomeia_turma_para_o_mesmo_nome(self):
        self.disciplina.criar_turma("A")
        self.disciplina.renomear_turma("A", "A")
        self.assertEqual(self.disciplina.buscar_turma("A").identificacao, "A")

    def test_remove_turma(self):
        self.disciplina.criar_turma("A")
        self.disciplina.remover_turma("A")
        with self.assertRaises(ErroRegistroNaoEncontrado):
            self.disciplina.buscar_turma("A")


class TesteTurma(unittest.TestCase):
    def setUp(self):
        self.turma = Disciplina("Compiladores", "COMP", 4).criar_turma("A")

    def test_rejeita_horarios_sobrepostos_na_mesma_turma(self):
        self.turma.adicionar_horario(criar_horario(DiaSemana.TERCA, "19:00", "21:00"))
        with self.assertRaises(ErroDadosInvalidos):
            self.turma.adicionar_horario(criar_horario(DiaSemana.TERCA, "20:00", "22:00"))

    def test_substitui_horario(self):
        atual = criar_horario(DiaSemana.TERCA, "19:00", "21:00")
        novo = criar_horario(DiaSemana.TERCA, "20:00", "22:00")
        self.turma.adicionar_horario(atual)
        self.turma.substituir_horario(atual, novo)
        self.assertEqual(self.turma.horarios, (novo,))

    def test_mantem_horario_quando_substituicao_falha(self):
        primeiro = criar_horario(DiaSemana.TERCA, "08:00", "10:00")
        segundo = criar_horario(DiaSemana.TERCA, "19:00", "21:00")
        self.turma.adicionar_horario(primeiro)
        self.turma.adicionar_horario(segundo)
        with self.assertRaises(ErroDadosInvalidos):
            self.turma.substituir_horario(segundo, criar_horario(DiaSemana.TERCA, "09:00", "11:00"))
        self.assertEqual(self.turma.horarios, (primeiro, segundo))

    def test_lista_horarios_em_ordem(self):
        quarta = criar_horario(DiaSemana.QUARTA, "19:00", "22:00")
        segunda = criar_horario(DiaSemana.SEGUNDA, "19:00", "22:00")
        self.turma.adicionar_horario(quarta)
        self.turma.adicionar_horario(segunda)
        self.assertEqual(self.turma.horarios, (segunda, quarta))
