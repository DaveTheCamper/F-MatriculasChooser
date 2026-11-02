from rematriculador.model.catalogo_disciplinas import CatalogoDisciplinas
from rematriculador.model.dia_semana import DiaSemana
from rematriculador.model.disciplina import Disciplina
from rematriculador.model.distribuicao_dias import DistribuicaoDias
from rematriculador.model.hora_do_dia import HoraDoDia
from rematriculador.model.horario import Horario
from rematriculador.model.planejamento import Planejamento
from rematriculador.model.preferencias_aluno import PreferenciasAluno
from rematriculador.model.turno import Turno


class MapeadorPlanejamento:
    def para_dicionario(self, planejamento):
        return {
            "disciplinas": [
                self.__disciplina_para_dicionario(disciplina)
                for disciplina in planejamento.catalogo.disciplinas
            ],
            "preferencias": self.__preferencias_para_dicionario(planejamento.preferencias),
        }

    def de_dicionario(self, dados):
        catalogo = CatalogoDisciplinas()
        for dados_disciplina in dados["disciplinas"]:
            catalogo.adicionar(self.__disciplina_de_dicionario(dados_disciplina))
        return Planejamento(catalogo, self.__preferencias_de_dicionario(dados["preferencias"]))

    def __disciplina_para_dicionario(self, disciplina):
        return {
            "nome": disciplina.nome,
            "codigo": disciplina.codigo,
            "prioridade": disciplina.prioridade,
            "turmas": [self.__turma_para_dicionario(turma) for turma in disciplina.turmas],
        }

    def __turma_para_dicionario(self, turma):
        return {
            "identificacao": turma.identificacao,
            "horarios": [self.__horario_para_dicionario(horario) for horario in turma.horarios],
        }

    def __horario_para_dicionario(self, horario):
        return {
            "dia": horario.dia.name,
            "inicio": str(horario.inicio),
            "termino": str(horario.termino),
        }

    def __preferencias_para_dicionario(self, preferencias):
        return {
            "turnos_preferidos": sorted(turno.name for turno in preferencias.turnos_preferidos),
            "distribuicao": preferencias.distribuicao.name,
            "quantidade_minima_disciplinas": preferencias.quantidade_minima_disciplinas,
        }

    def __disciplina_de_dicionario(self, dados):
        disciplina = Disciplina(dados["nome"], dados["codigo"], dados["prioridade"])
        for dados_turma in dados["turmas"]:
            turma = disciplina.criar_turma(dados_turma["identificacao"])
            for dados_horario in dados_turma["horarios"]:
                turma.adicionar_horario(self.__horario_de_dicionario(dados_horario))
        return disciplina

    def __horario_de_dicionario(self, dados):
        return Horario(
            DiaSemana[dados["dia"]],
            HoraDoDia.a_partir_de_texto(dados["inicio"]),
            HoraDoDia.a_partir_de_texto(dados["termino"]),
        )

    def __preferencias_de_dicionario(self, dados):
        return PreferenciasAluno(
            frozenset(Turno[nome] for nome in dados["turnos_preferidos"]),
            DistribuicaoDias[dados["distribuicao"]],
            dados["quantidade_minima_disciplinas"],
        )
