from dataclasses import dataclass, field

from rematriculador.model.catalogo_disciplinas import CatalogoDisciplinas
from rematriculador.model.preferencias_aluno import PreferenciasAluno


@dataclass
class Planejamento:
    catalogo: CatalogoDisciplinas = field(default_factory=CatalogoDisciplinas)
    preferencias: PreferenciasAluno = field(default_factory=PreferenciasAluno)
