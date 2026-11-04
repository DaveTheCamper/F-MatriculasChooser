from pathlib import Path
from tkinter import messagebox

from rematriculador.criterio.fabrica_criterios import FabricaCriterios
from rematriculador.model.excecoes import ErroPersistencia
from rematriculador.repository.repositorio_json import RepositorioJson
from rematriculador.service.planejador_grade import PlanejadorGrade
from rematriculador.service.servico_planejamento import ServicoPlanejamento
from rematriculador.view.aplicacao import Aplicacao

PASTA_DADOS = Path(__file__).resolve().parent / "dados"


def criar_servico():
    repositorio = RepositorioJson(PASTA_DADOS / "planejamento.json")
    repositorio_exemplo = RepositorioJson(PASTA_DADOS / "exemplo.json")
    return ServicoPlanejamento(repositorio, repositorio_exemplo, PlanejadorGrade(), FabricaCriterios())


def main():
    try:
        servico = criar_servico()
    except ErroPersistencia as erro:
        messagebox.showerror("Erro ao abrir os dados", str(erro))
        return
    Aplicacao(servico).mainloop()


if __name__ == "__main__":
    main()
