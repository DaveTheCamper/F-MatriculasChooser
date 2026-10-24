from rematriculador.model.excecoes import (
    ErroDadosInvalidos,
    ErroRegistroNaoEncontrado,
)


class Turma:
    def __init__(self, identificacao, disciplina):
        self.__disciplina = disciplina
        self.__horarios = []
        self.renomear(identificacao)

    @property
    def identificacao(self):
        return self.__identificacao

    @property
    def disciplina(self):
        return self.__disciplina

    @property
    def horarios(self):
        return tuple(sorted(self.__horarios, key=lambda horario: horario.chave_de_ordenacao()))

    def renomear(self, identificacao):
        identificacao_limpa = identificacao.strip()
        if not identificacao_limpa:
            raise ErroDadosInvalidos("Informe a identificação da turma.")
        self.__identificacao = identificacao_limpa

    def adicionar_horario(self, horario):
        self.__validar_novo_horario(horario, self.__horarios)
        self.__horarios.append(horario)

    def substituir_horario(self, horario_atual, novo_horario):
        self.__garantir_que_existe(horario_atual)
        demais_horarios = [horario for horario in self.__horarios if horario != horario_atual]
        self.__validar_novo_horario(novo_horario, demais_horarios)
        self.__horarios = [*demais_horarios, novo_horario]

    def remover_horario(self, horario):
        self.__garantir_que_existe(horario)
        self.__horarios.remove(horario)

    def possui_horarios(self):
        return bool(self.__horarios)

    def se_sobrepoe(self, outra_turma):
        return any(
            horario.se_sobrepoe(outro_horario)
            for horario in self.__horarios
            for outro_horario in outra_turma.horarios
        )

    def __validar_novo_horario(self, novo_horario, horarios_existentes):
        if any(novo_horario.se_sobrepoe(horario) for horario in horarios_existentes):
            raise ErroDadosInvalidos("Este horário se sobrepõe a outro horário da mesma turma.")

    def __garantir_que_existe(self, horario):
        if horario not in self.__horarios:
            raise ErroRegistroNaoEncontrado("Horário não encontrado nesta turma.")
