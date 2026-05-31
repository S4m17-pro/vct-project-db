from pydantic import BaseModel
from typing import Optional


class TorneoCreate(BaseModel):
    nombre_torneo: str
    region: Optional[str] = "Global"
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    ubicacion: Optional[str] = None
    premio_total: Optional[int] = 0


class TorneoUpdate(BaseModel):
    nombre_torneo: Optional[str] = None
    region: Optional[str] = None
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    ubicacion: Optional[str] = None
    premio_total: Optional[int] = None
