from rematriculador.model.aula import Aula
from rematriculador.model.excecoes import ErroDadosInvalidos
from rematriculador.model.hora_do_dia import MINUTOS_POR_HORA


class GradeHoraria:
    def __init__(self, turmas=()):
        self.__turmas = []
        for turma in turmas:
            self.adicionar(turma)

    @property
    def turmas(self):
        return tuple(self.__turmas)

    def aceita(self, turma):
        return not self.__repete_disciplina(turma) and not self.__tem_conflito(turma)

    def adicionar(self, turma):
        if not self.aceita(turma):
            raise ErroDadosInvalidos(
                f"A turma '{turma.identificacao}' não é compatível com esta grade."
            )
        self.__turmas.append(turma)

    def com_turma(self, turma):
        return GradeHoraria([*self.__turmas, turma])

    def quantidade_disciplinas(self):
        return len(self.__turmas)

    def soma_prioridades(self):
        return sum(turma.disciplina.prioridade for turma in self.__turmas)

    def aulas(self):
        aulas = [Aula(turma, horario) for turma in self.__turmas for horario in turma.horarios]
        return sorted(aulas, key=lambda aula: aula.horario.chave_de_ordenacao())

    def quantidade_aulas(self):
        return len(self.aulas())

    def quantidade_dias_ocupados(self):
        return len(self.__ordens_dos_dias_ocupados())

    def dias_vazios_no_meio(self):
        ordens = self.__ordens_dos_dias_ocupados()
        if not ordens:
            return 0
        return max(ordens) - min(ordens) + 1 - len(ordens)

    def horas_de_intervalo(self):
        aulas = self.aulas()
        minutos = sum(
            self.__minutos_entre(aula, proxima_aula)
            for aula, proxima_aula in zip(aulas, aulas[1:])
            if aula.horario.dia == proxima_aula.horario.dia
        )
        return minutos / MINUTOS_POR_HORA

    def proporcao_de_aulas_nos_turnos(self, turnos):
        aulas = self.aulas()
        if not aulas:
            return 0.0
        aulas_nos_turnos = [aula for aula in aulas if aula.horario.turno in turnos]
        return len(aulas_nos_turnos) / len(aulas)

    def __repete_disciplina(self, turma):
        return any(existente.disciplina is turma.disciplina for existente in self.__turmas)

    def __tem_conflito(self, turma):
        return any(existente.se_sobrepoe(turma) for existente in self.__turmas)

    def __ordens_dos_dias_ocupados(self):
        return {aula.horario.dia.ordem for aula in self.aulas()}

    def __minutos_entre(self, aula, proxima_aula):
        return aula.horario.termino.minutos_ate(proxima_aula.horario.inicio)
