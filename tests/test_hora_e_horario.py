import unittest

from rematriculador.model.dia_semana import DiaSemana
from rematriculador.model.excecoes import ErroDadosInvalidos
from rematriculador.model.hora_do_dia import HoraDoDia
from rematriculador.model.horario import Horario
from rematriculador.model.turno import Turno


def criar_horario(dia, inicio, termino):
    return Horario(dia, HoraDoDia.a_partir_de_texto(inicio), HoraDoDia.a_partir_de_texto(termino))


class TesteHoraDoDia(unittest.TestCase):
    def test_converte_texto_em_minutos(self):
        self.assertEqual(HoraDoDia.a_partir_de_texto("19:30").minutos_desde_meia_noite, 1170)

    def test_formata_com_dois_digitos(self):
        self.assertEqual(str(HoraDoDia.a_partir_de_texto("8:05")), "08:05")

    def test_rejeita_textos_invalidos(self):
        for texto in ("", "abc", "25:00", "10:75", "10h30"):
            with self.subTest(texto=texto):
                with self.assertRaises(ErroDadosInvalidos):
                    HoraDoDia.a_partir_de_texto(texto)


class TesteHorario(unittest.TestCase):
    def test_rejeita_termino_antes_do_inicio(self):
        with self.assertRaises(ErroDadosInvalidos):
            criar_horario(DiaSemana.SEGUNDA, "22:00", "19:00")

    def test_detecta_sobreposicao_parcial(self):
        primeiro = criar_horario(DiaSemana.TERCA, "19:00", "21:00")
        segundo = criar_horario(DiaSemana.TERCA, "20:00", "22:00")
        self.assertTrue(primeiro.se_sobrepoe(segundo))

    def test_horarios_encostados_nao_se_sobrepoem(self):
        primeiro = criar_horario(DiaSemana.TERCA, "08:30", "10:10")
        segundo = criar_horario(DiaSemana.TERCA, "10:10", "12:00")
        self.assertFalse(primeiro.se_sobrepoe(segundo))

    def test_dias_diferentes_nao_se_sobrepoem(self):
        primeiro = criar_horario(DiaSemana.TERCA, "19:00", "22:00")
        segundo = criar_horario(DiaSemana.QUARTA, "19:00", "22:00")
        self.assertFalse(primeiro.se_sobrepoe(segundo))

    def test_calcula_turno_pelo_inicio(self):
        self.assertIs(criar_horario(DiaSemana.SEXTA, "08:30", "10:00").turno, Turno.MANHA)
        self.assertIs(criar_horario(DiaSemana.SEXTA, "13:30", "15:00").turno, Turno.TARDE)
        self.assertIs(criar_horario(DiaSemana.SEXTA, "19:00", "22:00").turno, Turno.NOITE)
