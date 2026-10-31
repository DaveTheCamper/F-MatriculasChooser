import unittest

from rematriculador.criterio.criterio_avaliacao import CriterioAvaliacao
from rematriculador.criterio.criterio_distribuicao import CriterioDistribuicao
from rematriculador.criterio.criterio_prioridade import CriterioPrioridade
from rematriculador.criterio.criterio_turno import CriterioTurno
from rematriculador.model.dia_semana import DiaSemana
from rematriculador.model.distribuicao_dias import DistribuicaoDias
from rematriculador.model.grade_horaria import GradeHoraria
from rematriculador.model.turno import Turno
from tests.test_grade_horaria import criar_turma
from tests.test_hora_e_horario import criar_horario


class TesteCriterios(unittest.TestCase):
    def setUp(self):
        self.segunda = criar_turma("A", 3, criar_horario(DiaSemana.SEGUNDA, "19:00", "22:00"))
        self.quinta = criar_turma("B", 1, criar_horario(DiaSemana.QUINTA, "08:00", "10:00"))
        self.grade = GradeHoraria([self.segunda, self.quinta])

    def test_classe_base_nao_pode_ser_instanciada(self):
        with self.assertRaises(TypeError):
            CriterioAvaliacao(1.0)

    def test_prioridade_proporcional_ao_total(self):
        self.assertEqual(CriterioPrioridade(8).pontuar(self.grade), 50.0)

    def test_prioridade_sem_disciplinas_vale_zero(self):
        self.assertEqual(CriterioPrioridade(0).pontuar(GradeHoraria()), 0.0)

    def test_distribuicao_penaliza_dias_vazios(self):
        criterio = CriterioDistribuicao(DistribuicaoDias.EQUILIBRADA)
        self.assertEqual(criterio.pontuar(self.grade), 70.0)

    def test_distribuicao_concentrada_penaliza_dias_ocupados(self):
        criterio = CriterioDistribuicao(DistribuicaoDias.CONCENTRADA)
        self.assertEqual(criterio.pontuar(self.grade), 54.0)

    def test_turno_sem_preferencia_vale_maximo(self):
        self.assertEqual(CriterioTurno(frozenset()).pontuar(self.grade), 100.0)

    def test_turno_com_preferencia_usa_proporcao(self):
        self.assertEqual(CriterioTurno(frozenset({Turno.NOITE})).pontuar(self.grade), 50.0)

    def test_polimorfismo_aplica_o_peso_em_qualquer_criterio(self):
        criterios = [
            CriterioPrioridade(8, 0.5),
            CriterioDistribuicao(DistribuicaoDias.EQUILIBRADA, 0.5),
            CriterioTurno(frozenset({Turno.NOITE}), 0.5),
        ]
        pontuacoes = [criterio.avaliar(self.grade).pontuacao for criterio in criterios]
        self.assertEqual(pontuacoes, [25.0, 35.0, 25.0])
