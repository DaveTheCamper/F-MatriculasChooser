from rematriculador.model.grade_horaria import GradeHoraria
from rematriculador.model.grade_pontuada import GradePontuada

LIMITE_COMBINACOES = 20000


class PlanejadorGrade:
    def gerar_combinacoes(self, disciplinas, quantidade_minima):
        com_turmas = [disciplina for disciplina in disciplinas if disciplina.turmas_com_horario()]
        ordenadas = sorted(com_turmas, key=lambda disciplina: -disciplina.prioridade)
        combinacoes = []
        self.__explorar(ordenadas, GradeHoraria(), max(quantidade_minima, 1), combinacoes)
        return combinacoes

    def organizar(self, grades, criterios):
        pontuadas = [self.__pontuar(grade, criterios) for grade in grades]
        return sorted(pontuadas, key=lambda item: -item.pontuacao_total)

    def __explorar(self, restantes, grade, quantidade_minima, combinacoes):
        if len(combinacoes) >= LIMITE_COMBINACOES:
            return
        if grade.quantidade_disciplinas() + len(restantes) < quantidade_minima:
            return
        if not restantes:
            combinacoes.append(grade)
            return
        atual, *proximas = restantes
        for turma in atual.turmas_com_horario():
            if grade.aceita(turma):
                self.__explorar(proximas, grade.com_turma(turma), quantidade_minima, combinacoes)
        self.__explorar(proximas, grade, quantidade_minima, combinacoes)

    def __pontuar(self, grade, criterios):
        return GradePontuada(grade, tuple(criterio.avaliar(grade) for criterio in criterios))
