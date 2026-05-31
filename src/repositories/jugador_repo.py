from .base import BaseRepository


class JugadorRepository(BaseRepository):
    def insertar(self, nombre: str, pais: str = None, agente: str = None, id_equipo: str = None):
        return self._call_func_one(
            "sp_insertar_jugador",
            p_nombre=nombre, p_pais=pais,
            p_agente=agente, p_id_equipo=id_equipo
        )

    def actualizar(self, id_player: str, nombre: str = None, pais: str = None,
                   agente: str = None, id_equipo: str = None):
        return self._call_func_one(
            "sp_actualizar_jugador",
            p_id_player=id_player, p_nombre=nombre,
            p_pais=pais, p_agente=agente, p_id_equipo=id_equipo
        )

    def eliminar(self, id_player: str):
        self._call_proc("sp_eliminar_jugador", p_id_player=id_player)
