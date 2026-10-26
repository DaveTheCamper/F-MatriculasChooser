from rematriculador.model.excecoes import ErroRegistroDuplicado, ErroRegistroNaoEncontrado


class CatalogoDisciplinas:
    def __init__(self):
        self.__disciplinas = []

    @property
    def disciplinas(self):
        return tuple(self.__disciplinas)

    def adicionar(self, disciplina):
        self.garantir_codigo_livre(disciplina.codigo)
        self.__disciplinas.append(disciplina)

    def remover(self, codigo):
        self.__disciplinas.remove(self.buscar(codigo))

    def buscar(self, codigo):
        for disciplina in self.__disciplinas:
            if disciplina.codigo == codigo:
                return disciplina
        raise ErroRegistroNaoEncontrado(f"Disciplina '{codigo}' não encontrada.")

    def garantir_codigo_livre(self, codigo):
        if any(disciplina.codigo == codigo for disciplina in self.__disciplinas):
            raise ErroRegistroDuplicado(f"Já existe uma disciplina com o código '{codigo}'.")
