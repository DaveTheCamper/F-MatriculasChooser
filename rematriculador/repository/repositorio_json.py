import json

from rematriculador.model.excecoes import ErroPersistencia, ErroRematriculador
from rematriculador.model.planejamento import Planejamento
from rematriculador.repository.mapeador_planejamento import MapeadorPlanejamento
from rematriculador.repository.repositorio_planejamento import RepositorioPlanejamento


class RepositorioJson(RepositorioPlanejamento):
    def __init__(self, caminho_arquivo):
        self.__caminho_arquivo = caminho_arquivo
        self.__mapeador = MapeadorPlanejamento()

    def carregar(self):
        if not self.__caminho_arquivo.exists():
            return Planejamento()
        try:
            return self.__ler_arquivo()
        except (OSError, ValueError, KeyError, TypeError, ErroRematriculador) as erro:
            raise ErroPersistencia(
                f"Não foi possível ler o arquivo {self.__caminho_arquivo}: {erro}"
            ) from erro

    def salvar(self, planejamento):
        dados = self.__mapeador.para_dicionario(planejamento)
        texto = json.dumps(dados, ensure_ascii=False, indent=2)
        try:
            self.__caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
            self.__caminho_arquivo.write_text(texto, encoding="utf-8")
        except OSError as erro:
            raise ErroPersistencia(
                f"Não foi possível salvar o arquivo {self.__caminho_arquivo}: {erro}"
            ) from erro

    def __ler_arquivo(self):
        dados = json.loads(self.__caminho_arquivo.read_text(encoding="utf-8"))
        return self.__mapeador.de_dicionario(dados)
