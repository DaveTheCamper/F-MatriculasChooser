import unittest

from rematriculador.criterio.fabrica_criterios import FabricaCriterios
from rematriculador.model.excecoes import ErroRegistroDuplicado
from rematriculador.model.planejamento import Planejamento
from rematriculador.model.preferencias_aluno import PreferenciasAluno
from rematriculador.repository.repositorio_planejamento import RepositorioPlanejamento
from rematriculador.service.planejador_grade import PlanejadorGrade
from rematriculador.service.servico_planejamento import ServicoPlanejamento


class RepositorioEmMemoria(RepositorioPlanejamento):
    def __init__(self):
        self.quantidade_salvamentos = 0

    def carregar(self):
        return Planejamento()

    def salvar(self, planejamento):
        self.quantidade_salvamentos += 1


class TesteServicoPlanejamento(unittest.TestCase):
    def setUp(self):
        self.repositorio = RepositorioEmMemoria()
        self.servico = ServicoPlanejamento(
            self.repositorio, RepositorioEmMemoria(), PlanejadorGrade(), FabricaCriterios()
        )

    def test_cadastro_salva_automaticamente(self):
        self.servico.cadastrar_disciplina("Redes", "REDES", 2)
        self.assertEqual(self.repositorio.quantidade_salvamentos, 1)

    def test_nao_permite_codigo_duplicado(self):
        self.servico.cadastrar_disciplina("Redes", "REDES", 2)
        with self.assertRaises(ErroRegistroDuplicado):
            self.servico.cadastrar_disciplina("Outra", "redes", 3)

    def test_editar_para_codigo_existente_nao_altera_disciplina(self):
        self.servico.cadastrar_disciplina("Redes", "REDES", 2)
        self.servico.cadastrar_disciplina("Compiladores", "COMP", 4)
        with self.assertRaises(ErroRegistroDuplicado):
            self.servico.editar_disciplina("COMP", "Compiladores", "REDES", 4)
        self.assertEqual(self.servico.disciplinas[1].codigo, "COMP")

    def test_fluxo_completo_gera_grade_principal(self):
        self.servico.cadastrar_disciplina("Redes", "REDES", 2)
        self.servico.cadastrar_turma("REDES", "A")
        turma = self.servico.disciplinas[0].buscar_turma("A")
        self.servico.cadastrar_horario(turma, "Terça", "19:00", "22:00")
        grades = self.servico.gerar_grades()
        self.assertEqual(len(grades), 1)
        self.assertEqual(grades[0].grade.turmas, (turma,))

    def test_minimo_alto_nao_gera_grades(self):
        self.servico.cadastrar_disciplina("Redes", "REDES", 2)
        self.servico.cadastrar_turma("REDES", "A")
        turma = self.servico.disciplinas[0].buscar_turma("A")
        self.servico.cadastrar_horario(turma, "Terça", "19:00", "22:00")
        self.servico.atualizar_preferencias(PreferenciasAluno(quantidade_minima_disciplinas=2))
        self.assertEqual(self.servico.gerar_grades(), [])
