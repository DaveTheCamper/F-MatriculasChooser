class ErroRematriculador(Exception):
    pass


class ErroDadosInvalidos(ErroRematriculador):
    pass


class ErroRegistroDuplicado(ErroRematriculador):
    pass


class ErroRegistroNaoEncontrado(ErroRematriculador):
    pass


class ErroPersistencia(ErroRematriculador):
    pass
