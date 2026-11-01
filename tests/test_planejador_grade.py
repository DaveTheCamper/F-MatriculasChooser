import unittest

from rematriculador.criterio.criterio_prioridade import CriterioPrioridade
from rematriculador.model.dia_semana import DiaSemana
from rematriculador.model.disciplina import Disciplina
from rematriculador.service.planejador_grade import PlanejadorGrade
from tests.test_hora_e_horario import criar_horario


def criar_disciplina(codigo, prioridade, *horarios_das_turmas):
    disciplina = Disciplina(f"Disciplina {codigo}", codigo, prioridade)
    for indice, horario in enumerate(horarios_das_turmas):
        disciplina.criar_turma(f"T{indice}").adicionar_horario(horario)
    return disciplina


class TestePlanejadorGrade(unittest.TestCase):
    def setUp(self):
        self.planejador = PlanejadorGrade()
        self.terca = criar_horario(DiaSemana.TERCA, "19:00", "22:00")
        self.quarta = criar_horario(DiaSemana.QUARTA, "19:00", "22:00")

    def test_gera_todas_as_combinacoes_validas(self):
        primeira = criar_disciplina("A", 3, self.terca, self.quarta)
        segunda = criar_disciplina("B", 2, self.terca)
        combinacoes = self.planejador.gerar_combinacoes([primeira, segunda], 2)
        self.assertEqual(len(combinacoes), 1)
        self.assertEqual(combinacoes[0].turmas[0].identificacao, "T1")

    def test_considera_grades_parciais_acima_do_minimo(self):
        primeira = criar_disciplina("A", 3, self.terca)
        segunda = criar_disciplina("B", 2, self.quarta)
        self.assertEqual(len(self.planejador.gerar_combinacoes([primeira, segunda], 1)), 3)

    def test_retorna_vazio_quando_e_impossivel(self):
        primeira = criar_disciplina("A", 3, self.terca)
        segunda = criar_disciplina("B", 2, self.terca)
        self.assertEqual(self.planejador.gerar_combinacoes([primeira, segunda], 2), [])

    def test_ignora_turma_sem_horario(self):
        disciplina = Disciplina("Sem horário", "SH", 3)
        disciplina.criar_turma("A")
        self.assertEqual(self.planejador.gerar_combinacoes([disciplina], 1), [])

    def test_organiza_da_maior_para_a_menor_pontuacao(self):
        primeira = criar_disciplina("A", 5, self.terca)
        segunda = criar_disciplina("B", 1, self.quarta)
        grades = self.planejador.gerar_combinacoes([segunda, primeira], 1)
        organizadas = self.planejador.organizar(grades, [CriterioPrioridade(6)])
        pontuacoes = [round(item.pontuacao_total, 2) for item in organizadas]
        self.assertEqual(pontuacoes, [100.0, 83.33, 16.67])
