from rematriculador.model.dia_semana import DiaSemana
from rematriculador.model.disciplina import Disciplina
from rematriculador.model.hora_do_dia import HoraDoDia
from rematriculador.model.horario import Horario


class ServicoPlanejamento:
    def __init__(self, repositorio, repositorio_exemplo, planejador, fabrica_criterios):
        self.__repositorio = repositorio
        self.__repositorio_exemplo = repositorio_exemplo
        self.__planejador = planejador
        self.__fabrica_criterios = fabrica_criterios
        self.__planejamento = repositorio.carregar()

    @property
    def disciplinas(self):
        return self.__planejamento.catalogo.disciplinas

    @property
    def preferencias(self):
        return self.__planejamento.preferencias

    def cadastrar_disciplina(self, nome, codigo, prioridade):
        self.__catalogo().adicionar(Disciplina(nome, codigo, prioridade))
        self.__salvar()

    def editar_disciplina(self, codigo_atual, nome, codigo, prioridade):
        disciplina = self.__catalogo().buscar(codigo_atual)
        novo_codigo = codigo.strip().upper()
        if novo_codigo != codigo_atual:
            self.__catalogo().garantir_codigo_livre(novo_codigo)
        disciplina.atualizar(nome, codigo, prioridade)
        self.__salvar()

    def excluir_disciplina(self, codigo):
        self.__catalogo().remover(codigo)
        self.__salvar()

    def cadastrar_turma(self, codigo_disciplina, identificacao):
        self.__catalogo().buscar(codigo_disciplina).criar_turma(identificacao)
        self.__salvar()

    def editar_turma(self, codigo_disciplina, identificacao_atual, nova_identificacao):
        disciplina = self.__catalogo().buscar(codigo_disciplina)
        disciplina.renomear_turma(identificacao_atual, nova_identificacao)
        self.__salvar()

    def excluir_turma(self, codigo_disciplina, identificacao):
        self.__catalogo().buscar(codigo_disciplina).remover_turma(identificacao)
        self.__salvar()

    def cadastrar_horario(self, turma, rotulo_dia, inicio, termino):
        turma.adicionar_horario(self.__criar_horario(rotulo_dia, inicio, termino))
        self.__salvar()

    def editar_horario(self, turma, horario_atual, rotulo_dia, inicio, termino):
        turma.substituir_horario(horario_atual, self.__criar_horario(rotulo_dia, inicio, termino))
        self.__salvar()

    def excluir_horario(self, turma, horario):
        turma.remover_horario(horario)
        self.__salvar()

    def atualizar_preferencias(self, preferencias):
        self.__planejamento.preferencias = preferencias
        self.__salvar()

    def gerar_grades(self):
        grades = self.__planejador.gerar_combinacoes(
            self.disciplinas, self.preferencias.quantidade_minima_disciplinas
        )
        criterios = self.__fabrica_criterios.criar(self.disciplinas, self.preferencias)
        return self.__planejador.organizar(grades, criterios)

    def carregar_exemplo(self):
        self.__planejamento = self.__repositorio_exemplo.carregar()
        self.__salvar()

    def __catalogo(self):
        return self.__planejamento.catalogo

    def __criar_horario(self, rotulo_dia, inicio, termino):
        return Horario(
            DiaSemana.a_partir_de_rotulo(rotulo_dia),
            HoraDoDia.a_partir_de_texto(inicio),
            HoraDoDia.a_partir_de_texto(termino),
        )

    def __salvar(self):
        self.__repositorio.salvar(self.__planejamento)
