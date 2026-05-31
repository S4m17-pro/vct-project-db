from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy import Engine
from typing import List

from ..database import get_session
from ..dependencies import get_db, require_role
from ..schemas.jugador import JugadorCreate, JugadorUpdate
from ..models.schema import Jugador
from ..services.jugador_service import JugadorService
from ..repositories.jugador_repo import JugadorRepository

router = APIRouter(tags=["Jugadores"])


@router.get("/jugadores", response_model=List[Jugador])
def listar_jugadores(session: Session = Depends(get_session)):
    return session.exec(select(Jugador)).all()


@router.post("/jugadores", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_jugador(jugador_in: JugadorCreate, engine: Engine = Depends(get_db),
                  _=Depends(require_role("Admin"))):
    service = JugadorService(JugadorRepository(engine))
    result = service.crear(jugador_in.model_dump(exclude_none=True))
    if not result:
        raise HTTPException(status_code=500, detail="Error al insertar jugador")
    return {
        "id_player": result["id_player"],
        "nombre": result["nombre"],
        "pais": result["pais"],
        "agente": result["agente"],
        "id_equipo": result["id_equipo"],
    }


@router.put("/jugadores/{id_player}")
def modificar_jugador(id_player: str, jugador_data: JugadorUpdate,
                      engine: Engine = Depends(get_db),
                      _=Depends(require_role("Admin"))):
    service = JugadorService(JugadorRepository(engine))
    result = service.actualizar(id_player, jugador_data.model_dump(exclude_none=True))
    if not result:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"message": "Jugador modificado exitosamente", "jugador": result}


@router.delete("/jugadores/{id_player}")
def eliminar_jugador(id_player: str, engine: Engine = Depends(get_db),
                     _=Depends(require_role("Admin"))):
    service = JugadorService(JugadorRepository(engine))
    try:
        service.eliminar(id_player)
        return {"message": f"Jugador {id_player} eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
