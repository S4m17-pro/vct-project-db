from ..repositories.equipo_repo import EquipoRepository


class EquipoService:
    def __init__(self, repo: EquipoRepository):
        self._repo = repo

    def crear(self, data: dict):
        nombre = data.get("nombre_equipo") or data.get("Nombre_Equipo") or data.get("nombre")
        coach = data.get("coach") or data.get("Coach")
        region = data.get("region") or data.get("Region")
        return self._repo.insertar(nombre, coach, region)

    def actualizar(self, id_equipo: str, data: dict):
        nombre = data.get("nombre_equipo") or data.get("Nombre_Equipo") or data.get("nombre")
        coach = data.get("coach") or data.get("Coach")
        region = data.get("region") or data.get("Region")
        return self._repo.actualizar(id_equipo, nombre, coach, region)
