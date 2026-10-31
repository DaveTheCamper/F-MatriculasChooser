from rematriculador.criterio.criterio_avaliacao import CriterioAvaliacao, PONTUACAO_MAXIMA


class CriterioPrioridade(CriterioAvaliacao):
    def __init__(self, soma_total_prioridades, peso=1.0):
        super().__init__(peso)
        self.__soma_total_prioridades = soma_total_prioridades

    @property
    def nome(self):
        return "Prioridades"

    def pontuar(self, grade):
        if self.__soma_total_prioridades == 0:
            return 0.0
        return PONTUACAO_MAXIMA * grade.soma_prioridades() / self.__soma_total_prioridades
