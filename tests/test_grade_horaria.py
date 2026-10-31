import unittest

from rematriculador.model.dia_semana import DiaSemana
from rematriculador.model.disciplina import Disciplina
from rematriculador.model.excecoes import ErroDadosInvalidos
from rematriculador.model.grade_horaria import GradeHoraria
from rematriculador.model.turno import Turno
from tests.test_hora_e_horario import criar_horario


def criar_turma(codigo, prioridade, *horarios):
    turma = Disciplina(f"Disciplina {codigo}", codigo, prioridade).criar_turma("A")
    for horario in horarios:
        turma.adicionar_horario(horario)
    return turma


class TesteGradeHoraria(unittest.TestCase):
    def test_rejeita_turma_com_conflito(self):
        primeira = criar_turma("A", 1, criar_horario(DiaSemana.TERCA, "19:00", "22:00"))
        segunda = criar_turma("B", 1, criar_horario(DiaSemana.TERCA, "21:00", "23:00"))
        grade = GradeHoraria([primeira])
        self.assertFalse(grade.aceita(segunda))
        with self.assertRaises(ErroDadosInvalidos):
            grade.adicionar(segunda)

    def test_rejeita_segunda_turma_da_mesma_disciplina(self):
        disciplina = Disciplina("Redes", "REDES", 2)
        primeira = disciplina.criar_turma("A")
        segunda = disciplina.criar_turma("B")
        primeira.adicionar_horario(criar_horario(DiaSemana.TERCA, "19:00", "22:00"))
        segunda.adicionar_horario(criar_horario(DiaSemana.QUARTA, "19:00", "22:00"))
        self.assertFalse(GradeHoraria([primeira]).aceita(segunda))

    def test_com_turma_nao_altera_a_grade_original(self):
        turma = criar_turma("A", 1, criar_horario(DiaSemana.TERCA, "19:00", "22:00"))
        grade = GradeHoraria()
        nova_grade = grade.com_turma(turma)
        self.assertEqual(grade.quantidade_disciplinas(), 0)
        self.assertEqual(nova_grade.quantidade_disciplinas(), 1)

    def test_conta_dias_vazios_no_meio(self):
        segunda = criar_turma("A", 1, criar_horario(DiaSemana.SEGUNDA, "19:00", "22:00"))
        quinta = criar_turma("B", 1, criar_horario(DiaSemana.QUINTA, "19:00", "22:00"))
        self.assertEqual(GradeHoraria([segunda, quinta]).dias_vazios_no_meio(), 2)

    def test_grade_vazia_nao_tem_dias_vazios(self):
        self.assertEqual(GradeHoraria().dias_vazios_no_meio(), 0)

    def test_calcula_intervalo_apenas_no_mesmo_dia(self):
        manha = criar_turma("A", 1, criar_horario(DiaSemana.TERCA, "08:00", "10:00"))
        tarde = criar_turma("B", 1, criar_horario(DiaSemana.TERCA, "13:00", "15:00"))
        outro_dia = criar_turma("C", 1, criar_horario(DiaSemana.QUARTA, "19:00", "22:00"))
        self.assertEqual(GradeHoraria([manha, tarde, outro_dia]).horas_de_intervalo(), 3)

    def test_calcula_proporcao_nos_turnos(self):
        manha = criar_turma("A", 1, criar_horario(DiaSemana.TERCA, "08:00", "10:00"))
        noite = criar_turma("B", 1, criar_horario(DiaSemana.QUARTA, "19:00", "22:00"))
        grade = GradeHoraria([manha, noite])
        self.assertEqual(grade.proporcao_de_aulas_nos_turnos({Turno.NOITE}), 0.5)
