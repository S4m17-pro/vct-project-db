from pydantic import BaseModel
from typing import Optional


class LeaderboardRow(BaseModel):
    id_player: str
    jugador: str
    equipo: str
    total_kills: int
    total_deaths: int
    kdr: float


class MapStat(BaseModel):
    mapa: str
    jugadas: int
    victorias: int
    winrate: float


class WeaponStat(BaseModel):
    weapon: str
    type: str
    kills: int
    damage: int


class AgentPick(BaseModel):
    agent: str
    role: str
    pickRate: float


class PartidaRecuento(BaseModel):
    id_partida: str
    torneo: str
    fase: int
    mapa: str
    equipo_1: str
    equipo_2: str
    ganador: str
    score_equipo_1: int
    score_equipo_2: int
    duracion: str
    fecha: str
