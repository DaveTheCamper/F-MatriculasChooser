from rematriculador.model.excecoes import (
    ErroDadosInvalidos,
    ErroRegistroDuplicado,
    ErroRegistroNaoEncontrado,
)
from rematriculador.model.turma import Turma

PRIORIDADE_MINIMA = 1
PRIORIDADE_MAXIMA = 5


class Disciplina:
    def __init__(self, nome, codigo, prioridade=PRIORIDADE_MINIMA):
        self.__turmas = []
        self.atualizar(nome, codigo, prioridade)

    @property
    def nome(self):
        return self.__nome

    @property
    def codigo(self):
        return self.__codigo

    @property
    def prioridade(self):
        return self.__prioridade

    @property
    def turmas(self):
        return tuple(self.__turmas)

    def atualizar(self, nome, codigo, prioridade):
        nome_limpo = nome.strip()
        codigo_limpo = codigo.strip().upper()
        if not nome_limpo or not codigo_limpo:
            raise ErroDadosInvalidos("Informe o nome e o código da disciplina.")
        self.__validar_prioridade(prioridade)
        self.__nome = nome_limpo
        self.__codigo = codigo_limpo
        self.__prioridade = prioridade

    def criar_turma(self, identificacao):
        turma = Turma(identificacao, self)
        self.__garantir_identificacao_livre(turma.identificacao)
        self.__turmas.append(turma)
        return turma

    def renomear_turma(self, identificacao_atual, nova_identificacao):
        turma = self.buscar_turma(identificacao_atual)
        if nova_identificacao.strip() != turma.identificacao:
            self.__garantir_identificacao_livre(nova_identificacao.strip())
        turma.renomear(nova_identificacao)

    def remover_turma(self, identificacao):
        self.__turmas.remove(self.buscar_turma(identificacao))

    def buscar_turma(self, identificacao):
        for turma in self.__turmas:
            if turma.identificacao == identificacao:
                return turma
        raise ErroRegistroNaoEncontrado(f"Turma '{identificacao}' não encontrada.")

    def turmas_com_horario(self):
        return [turma for turma in self.__turmas if turma.possui_horarios()]

    def __garantir_identificacao_livre(self, identificacao):
        if any(turma.identificacao == identificacao for turma in self.__turmas):
            raise ErroRegistroDuplicado(f"A turma '{identificacao}' já existe nesta disciplina.")

    def __validar_prioridade(self, prioridade):
        if not PRIORIDADE_MINIMA <= prioridade <= PRIORIDADE_MAXIMA:
            raise ErroDadosInvalidos(
                f"A prioridade deve estar entre {PRIORIDADE_MINIMA} e {PRIORIDADE_MAXIMA}."
            )
