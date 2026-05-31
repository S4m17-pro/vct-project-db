from pydantic import BaseModel
from typing import Optional


class EquipoCreate(BaseModel):
    nombre_equipo: str
    coach: Optional[str] = None
    region: Optional[str] = None


class EquipoUpdate(BaseModel):
    nombre_equipo: Optional[str] = None
    coach: Optional[str] = None
    region: Optional[str] = None
