from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Engine

from ..dependencies import get_db, require_role
from ..schemas.partida import PartidaCreate, ProcedimientoPartidaInput
from ..services.partida_service import PartidaService
from ..repositories.partida_repo import PartidaRepository

router = APIRouter(tags=["Partidas"])


@router.post("/partidas")
def crear_partida(partida: PartidaCreate, engine: Engine = Depends(get_db),
                  _=Depends(require_role("Admin"))):
    service = PartidaService(PartidaRepository(engine))
    try:
        service.crear(partida.model_dump())
        return {"status": "success", "message": f"Partida {partida.id_partida} registrada."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/partidas/registrar")
def registrar_partida_completa(datos: ProcedimientoPartidaInput,
                               engine: Engine = Depends(get_db),
                               _=Depends(require_role("Admin"))):
    repo = PartidaRepository(engine)
    try:
        repo.registrar_completa(
            datos.p_id_partida, datos.p_fase, datos.p_id_torneo,
            datos.p_id_mapa, datos.p_id_equipo1, datos.p_id_equipo2,
            datos.p_score1, datos.p_score2, datos.p_duracion
        )
        return {"status": "success", "message": f"Partida {datos.p_id_partida} registrada."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
