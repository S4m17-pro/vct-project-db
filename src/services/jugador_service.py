from ..repositories.jugador_repo import JugadorRepository


class JugadorService:
    def __init__(self, repo: JugadorRepository):
        self._repo = repo

    def crear(self, data: dict):
        nombre = data.get("nombre") or data.get("Nombre")
        pais = data.get("pais") or data.get("Pais")
        agente = data.get("agente") or data.get("Agente")
        id_equipo = data.get("id_equipo") or data.get("Id_Equipo")
        return self._repo.insertar(nombre, pais, agente, id_equipo)

    def actualizar(self, id_player: str, data: dict):
        nombre = data.get("nombre") or data.get("Nombre")
        pais = data.get("pais") or data.get("Pais")
        agente = data.get("agente") or data.get("Agente")
        id_equipo = data.get("id_equipo") or data.get("Id_Equipo")
        return self._repo.actualizar(id_player, nombre, pais, agente, id_equipo)

    def eliminar(self, id_player: str):
        self._repo.eliminar(id_player)
