from rematriculador.criterio.criterio_avaliacao import CriterioAvaliacao, PONTUACAO_MAXIMA


class CriterioTurno(CriterioAvaliacao):
    def __init__(self, turnos_preferidos, peso=1.0):
        super().__init__(peso)
        self.__turnos_preferidos = turnos_preferidos

    @property
    def nome(self):
        return "Turnos"

    def pontuar(self, grade):
        if not self.__turnos_preferidos:
            return PONTUACAO_MAXIMA
        return PONTUACAO_MAXIMA * grade.proporcao_de_aulas_nos_turnos(self.__turnos_preferidos)
