from pydantic import BaseModel
from typing import Optional


class JugadorCreate(BaseModel):
    nombre: str
    pais: Optional[str] = None
    agente: Optional[str] = None
    id_equipo: Optional[str] = None


class JugadorUpdate(BaseModel):
    nombre: Optional[str] = None
    pais: Optional[str] = None
    agente: Optional[str] = None
    id_equipo: Optional[str] = None
