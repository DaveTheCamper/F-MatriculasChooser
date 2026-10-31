from rematriculador.criterio.criterio_avaliacao import CriterioAvaliacao, PONTUACAO_MAXIMA
from rematriculador.model.distribuicao_dias import DistribuicaoDias

PENALIDADE_POR_DIA_VAZIO = 15
PENALIDADE_POR_HORA_DE_INTERVALO = 5
PENALIDADE_POR_DIA_OCUPADO = 8
PENALIDADE_POR_AULA_EXTRA_NO_DIA = 10


class CriterioDistribuicao(CriterioAvaliacao):
    def __init__(self, distribuicao, peso=1.0):
        super().__init__(peso)
        self.__distribuicao = distribuicao

    @property
    def nome(self):
        return "Distribuição"

    def pontuar(self, grade):
        penalidade = (
            grade.dias_vazios_no_meio() * PENALIDADE_POR_DIA_VAZIO
            + grade.horas_de_intervalo() * PENALIDADE_POR_HORA_DE_INTERVALO
            + self.__penalidade_da_preferencia(grade)
        )
        return max(0.0, PONTUACAO_MAXIMA - penalidade)

    def __penalidade_da_preferencia(self, grade):
        if self.__distribuicao is DistribuicaoDias.CONCENTRADA:
            return grade.quantidade_dias_ocupados() * PENALIDADE_POR_DIA_OCUPADO
        aulas_extras = grade.quantidade_aulas() - grade.quantidade_dias_ocupados()
        return aulas_extras * PENALIDADE_POR_AULA_EXTRA_NO_DIA
