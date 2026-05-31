from ..repositories.analytics_repo import AnalyticsRepository


class AnalyticsService:
    def __init__(self, repo: AnalyticsRepository):
        self._repo = repo

    def leaderboard(self):
        rows = self._repo.leaderboard()
        return [
            {
                "id_player": r["id_player"],
                "jugador": r["jugador"],
                "equipo": r["equipo"] if r.get("equipo") else "Sin Equipo",
                "total_kills": r["total_kills"] or 0,
                "total_deaths": r["total_deaths"] or 0,
                "kdr": float(r["kdr"]) if r.get("kdr") else 0.0,
            }
            for r in rows
        ]

    def map_stats(self, id_equipo: str):
        rows = self._repo.map_stats_equipo(id_equipo)
        return [
            {
                "mapa": r["mapa"],
                "jugadas": int(r["jugadas"]),
                "victorias": int(r["victorias"]),
                "winrate": float(r["winrate"]) if r.get("winrate") else 0.0,
            }
            for r in rows
        ]

    def armas_jugador(self, id_player: str):
        rows = self._repo.armas_jugador(id_player)
        if not rows:
            return [
                {"weapon": "Vandal", "type": "Rifle", "kills": 0, "damage": 0},
                {"weapon": "Phantom", "type": "Rifle", "kills": 0, "damage": 0},
            ]
        return [
            {
                "weapon": r["weapon"],
                "type": r["tipo"],
                "kills": int(r["kills"]),
                "damage": int(r["damage"]),
            }
            for r in rows
        ]

    def meta_agentes(self):
        rows = self._repo.meta_agentes()
        return [
            {
                "agent": r["agent"],
                "role": r["role"],
                "pickRate": float(r["pickrate"]) if r.get("pickrate") else 0.0,
            }
            for r in rows
        ] if rows else []

    def recuento_partidas(self, torneo: str = None, fase: int = None):
        rows = self._repo.recuento_partidas(torneo, fase)
        return [
            {
                "id_partida": r["id_partida"],
                "torneo": r["torneo"],
                "fase": r["fase"],
                "mapa": r["mapa"],
                "equipo_1": r["equipo_1"],
                "equipo_2": r["equipo_2"],
                "ganador": r["ganador"] if r.get("ganador") else "Empate/Sin definir",
                "score_equipo_1": r["score_equipo_1"],
                "score_equipo_2": r["score_equipo_2"],
                "duracion": str(r["duracion"]),
                "fecha": str(r["fecha"]),
            }
            for r in rows
        ]
