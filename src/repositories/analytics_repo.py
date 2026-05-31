from .base import BaseRepository


class AnalyticsRepository(BaseRepository):
    def leaderboard(self):
        return self._call_func("sp_obtener_leaderboard")

    def map_stats_equipo(self, id_equipo: str):
        return self._call_func("sp_obtener_map_stats_equipo", p_id_equipo=id_equipo)

    def armas_jugador(self, id_player: str):
        return self._call_func("sp_obtener_armas_jugador", p_id_player=id_player)

    def meta_agentes(self):
        return self._call_func("sp_obtener_meta_agentes")

    def recuento_partidas(self, torneo: str = None, fase: int = None):
        return self._call_func(
            "sp_obtener_recuento_partidas",
            p_torneo=torneo, p_fase=fase
        )
