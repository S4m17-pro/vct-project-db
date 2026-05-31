from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import Engine
from typing import List, Optional

from ..database import get_session
from ..dependencies import get_db
from ..schemas.analytics import LeaderboardRow, MapStat, WeaponStat, AgentPick, PartidaRecuento
from ..models.schema import Vista_Resumen_Jugadores, Vista_Estadisticas_Equipos, Audit_Log, Vista_Meta_Agentes
from ..services.analytics_service import AnalyticsService
from ..repositories.analytics_repo import AnalyticsRepository

router = APIRouter(tags=["Valorant Tracker - Insights"])


@router.get("/jugadores/resumen")
def obtener_resumen_jugadores(session: Session = Depends(get_session)):
    return session.exec(select(Vista_Resumen_Jugadores)).all()


@router.get("/equipos/estadisticas")
def obtener_estadisticas_equipos(session: Session = Depends(get_session)):
    return session.exec(select(Vista_Estadisticas_Equipos)).all()


@router.get("/auditoria")
def ver_logs_auditoria(session: Session = Depends(get_session)):
    return session.exec(select(Audit_Log).order_by(Audit_Log.id_audit.desc())).all()


@router.get("/analytics/leaderboard")
def obtener_leaderboard(engine: Engine = Depends(get_db)):
    service = AnalyticsService(AnalyticsRepository(engine))
    return service.leaderboard()


@router.get("/analytics/equipos/{id_equipo}/map-stats")
def stats_mapas_equipo(id_equipo: str, engine: Engine = Depends(get_db)):
    service = AnalyticsService(AnalyticsRepository(engine))
    return service.map_stats(id_equipo)


@router.get("/analytics/jugadores/{id_player}/armas")
def obtener_armas_jugador(id_player: str, engine: Engine = Depends(get_db)):
    service = AnalyticsService(AnalyticsRepository(engine))
    return service.armas_jugador(id_player)


@router.get("/analytics/meta/agentes")
def obtener_pickrate_agentes(engine: Engine = Depends(get_db)):
    service = AnalyticsService(AnalyticsRepository(engine))
    return service.meta_agentes()


@router.get("/analytics/partidas/recuento")
def obtener_recuento_partidas(torneo: Optional[str] = None, fase: Optional[int] = None,
                              engine: Engine = Depends(get_db)):
    service = AnalyticsService(AnalyticsRepository(engine))
    return service.recuento_partidas(torneo, fase)
