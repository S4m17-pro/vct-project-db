from ..repositories.partida_repo import PartidaRepository


class PartidaService:
    def __init__(self, repo: PartidaRepository):
        self._repo = repo

    def crear(self, data: dict):
        return self._repo.insertar(
            id_partida=data.get("id_partida"),
            fecha=data.get("fecha"),
            fase=data.get("fase"),
            id_torneofk=data.get("id_torneofk"),
            id_equipo1=data.get("id_equipo1"),
            id_equipo2=data.get("id_equipo2"),
            id_equipo_ganador=data.get("id_equipo_ganador"),
        )
