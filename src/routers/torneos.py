from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import Engine
from typing import List

from ..database import get_session
from ..dependencies import get_db, require_role
from ..schemas.torneo import TorneoCreate, TorneoUpdate
from ..models.schema import Torneo
from ..services.partida_service import PartidaService
from ..repositories.torneo_repo import TorneoRepository

router = APIRouter(tags=["Torneos"])


@router.get("/torneos")
def listar_torneos(engine: Engine = Depends(get_db)):
    repo = TorneoRepository(engine)
    rows = repo.obtener_todos()
    return [
        {
            "id_torneo": r["id_torneo"],
            "nombre": r["nombre"],
            "anio": int(r["anio"]) if r.get("anio") else 2026,
            "region": r["region"] if r.get("region") else "Global",
        }
        for r in rows
    ]


@router.post("/torneos")
def crear_torneo(torneo_data: TorneoCreate, session: Session = Depends(get_session),
                 _=Depends(require_role("Admin"))):
    db_torneo = Torneo(
        id_torneo=f"T{len(session.exec(select(Torneo)).all()) + 1:02d}",
        nombre_torneo=torneo_data.nombre_torneo,
        region=torneo_data.region,
        fecha_inicio=torneo_data.fecha_inicio,
        fecha_fin=torneo_data.fecha_fin,
        ubicacion=torneo_data.ubicacion,
        premio_total=torneo_data.premio_total,
    )
    session.add(db_torneo)
    session.commit()
    session.refresh(db_torneo)
    return {"message": "Torneo creado exitosamente", "id_torneo": db_torneo.id_torneo}


@router.put("/torneos/{id_torneo}")
def modificar_torneo(id_torneo: str, torneo_data: TorneoUpdate,
                     session: Session = Depends(get_session),
                     _=Depends(require_role("Admin"))):
    db_torneo = session.get(Torneo, id_torneo)
    if not db_torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    data = torneo_data.model_dump(exclude_none=True)
    for attr in ("nombre_torneo", "region", "fecha_inicio", "fecha_fin", "ubicacion", "premio_total"):
        if attr in data:
            setattr(db_torneo, attr, data[attr])
    session.add(db_torneo)
    session.commit()
    session.refresh(db_torneo)
    return {"message": "Torneo modificado exitosamente", "torneo": db_torneo.model_dump()}


@router.delete("/torneos/{id_torneo}")
def eliminar_torneo(id_torneo: str, session: Session = Depends(get_session),
                    _=Depends(require_role("Admin"))):
    db_torneo = session.get(Torneo, id_torneo)
    if not db_torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    session.delete(db_torneo)
    session.commit()
    return {"message": f"Torneo {id_torneo} eliminado correctamente"}
