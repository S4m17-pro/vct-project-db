from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import Engine
from typing import List

from ..database import get_session
from ..dependencies import get_db, require_role
from ..schemas.equipo import EquipoCreate, EquipoUpdate
from ..models.schema import Equipo
from ..services.equipo_service import EquipoService
from ..repositories.equipo_repo import EquipoRepository

router = APIRouter(tags=["Equipos"])


@router.get("/equipos")
def listar_equipos(session: Session = Depends(get_session)):
    rows = session.exec(select(Equipo)).all()
    return [
        {
            "id_equipo": str(r.id_equipo),
            "nombre": r.nombre_equipo,
            "region": r.region,
            "coach": r.coach,
        }
        for r in rows
    ]


@router.post("/equipos")
def crear_equipo(equipo_data: EquipoCreate, engine: Engine = Depends(get_db),
                 _=Depends(require_role("Admin"))):
    service = EquipoService(EquipoRepository(engine))
    result = service.crear(equipo_data.model_dump(exclude_none=True))
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear equipo")
    return {"status": "success", "message": f"Equipo '{result['nombre_equipo']}' registrado."}


@router.put("/equipos/{id_equipo}")
def modificar_equipo(id_equipo: str, equipo_data: EquipoUpdate,
                     engine: Engine = Depends(get_db),
                     _=Depends(require_role("Admin"))):
    service = EquipoService(EquipoRepository(engine))
    result = service.actualizar(id_equipo, equipo_data.model_dump(exclude_none=True))
    if not result:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"status": "success", "message": f"Equipo {id_equipo} modificado."}
