from pydantic import BaseModel
from typing import Optional
from datetime import date


class TorneoCreate(BaseModel):
    nombre_torneo: str
    region: Optional[str] = "Global"
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    ubicacion: Optional[str] = None
    premio_total: Optional[int] = 0


class TorneoUpdate(BaseModel):
    nombre_torneo: Optional[str] = None
    region: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    ubicacion: Optional[str] = None
    premio_total: Optional[int] = None
