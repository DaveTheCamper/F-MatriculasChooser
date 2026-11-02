import tempfile
import unittest
from pathlib import Path

from rematriculador.model.dia_semana import DiaSemana
from rematriculador.model.disciplina import Disciplina
from rematriculador.model.distribuicao_dias import DistribuicaoDias
from rematriculador.model.excecoes import ErroPersistencia
from rematriculador.model.planejamento import Planejamento
from rematriculador.model.preferencias_aluno import PreferenciasAluno
from rematriculador.model.turno import Turno
from rematriculador.repository.repositorio_json import RepositorioJson
from tests.test_hora_e_horario import criar_horario


class TesteRepositorioJson(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.caminho = Path(self.pasta.name) / "dados" / "planejamento.json"
        self.repositorio = RepositorioJson(self.caminho)

    def test_arquivo_inexistente_gera_planejamento_vazio(self):
        self.assertEqual(self.repositorio.carregar().catalogo.disciplinas, ())

    def test_salva_e_recupera_os_dados(self):
        disciplina = Disciplina("Programação Orientada a Objetos", "POO", 5)
        horario = criar_horario(DiaSemana.QUINTA, "19:00", "22:00")
        disciplina.criar_turma("A").adicionar_horario(horario)
        planejamento = Planejamento(
            preferencias=PreferenciasAluno(frozenset({Turno.NOITE}), DistribuicaoDias.CONCENTRADA, 2)
        )
        planejamento.catalogo.adicionar(disciplina)

        self.repositorio.salvar(planejamento)
        recuperado = self.repositorio.carregar()

        disciplina_recuperada = recuperado.catalogo.buscar("POO")
        self.assertEqual(disciplina_recuperada.nome, "Programação Orientada a Objetos")
        self.assertEqual(disciplina_recuperada.buscar_turma("A").horarios, (horario,))
        self.assertEqual(recuperado.preferencias, planejamento.preferencias)

    def test_arquivo_corrompido_gera_erro_de_persistencia(self):
        self.caminho.parent.mkdir(parents=True)
        self.caminho.write_text("{ isso não é json", encoding="utf-8")
        with self.assertRaises(ErroPersistencia):
            self.repositorio.carregar()

    def test_exemplo_do_projeto_pode_ser_carregado(self):
        caminho_exemplo = Path(__file__).resolve().parent.parent / "dados" / "exemplo.json"
        planejamento = RepositorioJson(caminho_exemplo).carregar()
        self.assertEqual(len(planejamento.catalogo.disciplinas), 9)
