from .base import BaseRepository


class EquipoRepository(BaseRepository):
    def insertar(self, nombre_equipo: str, coach: str = None, region: str = None):
        return self._call_func_one(
            "sp_insertar_equipo",
            p_nombre_equipo=nombre_equipo, p_coach=coach, p_region=region
        )

    def actualizar(self, id_equipo: str, nombre_equipo: str = None,
                   coach: str = None, region: str = None):
        return self._call_func_one(
            "sp_actualizar_equipo",
            p_id_equipo=id_equipo, p_nombre_equipo=nombre_equipo,
            p_coach=coach, p_region=region
        )
