from pydantic import BaseModel
from typing import Optional
from datetime import date


class PartidaCreate(BaseModel):
    id_partida: str
    fecha: date
    fase: int
    id_torneofk: str
    id_equipo1: str
    id_equipo2: str
    id_equipo_ganador: str


class ProcedimientoPartidaInput(BaseModel):
    p_id_partida: str
    p_fase: int
    p_id_torneo: str
    p_id_mapa: str
    p_id_equipo1: str
    p_id_equipo2: str
    p_score1: int
    p_score2: int
    p_duracion: int | str
