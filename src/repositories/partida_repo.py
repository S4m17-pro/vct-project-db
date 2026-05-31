from .base import BaseRepository


class PartidaRepository(BaseRepository):
    def insertar(self, id_partida: str, fecha, fase: int, id_torneofk: str,
                 id_equipo1: str, id_equipo2: str, id_equipo_ganador: str):
        return self._call_func_one(
            "sp_insertar_partida",
            p_id_partida=id_partida, p_fecha=fecha, p_fase=fase,
            p_id_torneofk=id_torneofk, p_id_equipo1=id_equipo1,
            p_id_equipo2=id_equipo2, p_id_equipo_ganador=id_equipo_ganador
        )

    def actualizar(self, id_partida: str, fecha=None, fase: int = None, id_torneofk: str = None):
        return self._call_func_one(
            "sp_actualizar_partida",
            p_id_partida=id_partida, p_fecha=fecha,
            p_fase=fase, p_id_torneofk=id_torneofk
        )

    def registrar_completa(self, p_id_partida: str, p_fase: int, p_id_torneo: str,
                           p_id_mapa: str, p_id_equipo1: str, p_id_equipo2: str,
                           p_score1: int, p_score2: int, p_duracion):
        if isinstance(p_duracion, int):
            duracion_str = f"{p_duracion // 60:02d}:{p_duracion % 60:02d}:00"
        else:
            duracion_str = str(p_duracion)
        self._call_proc(
            "sp_registrar_partida",
            p_id_partida=p_id_partida, p_fase=p_fase, p_id_torneo=p_id_torneo,
            p_id_mapa=p_id_mapa, p_id_equipo1=p_id_equipo1, p_id_equipo2=p_id_equipo2,
            p_score1=p_score1, p_score2=p_score2, p_duracion=duracion_str
        )
