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
        Id_Torneo=f"T{len(session.exec(select(Torneo)).all()) + 1:02d}",
        nombre_torneo=torneo_data.nombre_torneo,
        Region=torneo_data.region,
        Fecha_inicio=torneo_data.fecha_inicio,
        Fecha_fin=torneo_data.fecha_fin,
        Ubicacion=torneo_data.ubicacion,
        Premio_total=torneo_data.premio_total,
    )
    session.add(db_torneo)
    session.commit()
    session.refresh(db_torneo)
    return {"message": "Torneo creado exitosamente", "id_torneo": db_torneo.Id_Torneo}


@router.put("/torneos/{id_torneo}")
def modificar_torneo(id_torneo: str, torneo_data: TorneoUpdate,
                     session: Session = Depends(get_session),
                     _=Depends(require_role("Admin"))):
    db_torneo = session.get(Torneo, id_torneo)
    if not db_torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    data = torneo_data.model_dump(exclude_none=True)
    if "nombre_torneo" in data:
        db_torneo.nombre_torneo = data["nombre_torneo"]
    if "region" in data:
        db_torneo.Region = data["region"]
    if "fecha_inicio" in data:
        db_torneo.Fecha_inicio = data["fecha_inicio"]
    if "fecha_fin" in data:
        db_torneo.Fecha_fin = data["fecha_fin"]
    if "ubicacion" in data:
        db_torneo.Ubicacion = data["ubicacion"]
    if "premio_total" in data:
        db_torneo.Premio_total = data["premio_total"]
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
