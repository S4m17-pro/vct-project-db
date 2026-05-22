import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, text  # 'text' ya está incluido aquí para evitar errores
from typing import List
from database import engine, get_session

# Importaciones directas y limpias sin prefijos molestos
from database import get_session
from models import (
    Vista_Resumen_Jugadores,
    Vista_Estadisticas_Equipos,
    Jugador,
    JugadorCreate,
    Audit_Log,
    ProcedimientoPartidaInput
)

# Inicialización de la API
app = FastAPI(
    title="VCT Stats API - Universidad Libre",
    description="Backend definitivo sintonizado con tu base de datos de Docker",
    version="3.0"
)

# Configuración de CORS para conectarte con Lovable o el navegador sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "ok", 
        "message": "Backend de FastAPI corriendo perfectamente y listo para usar"
    }

# ==========================================
# 📊 ENDPOINTS PARA VISTAS (01-views.sql)
# ==========================================

@app.get("/jugadores/resumen", response_model=List[Vista_Resumen_Jugadores])
def obtener_resumen_jugadores(session: Session = Depends(get_session)):
    """Retorna el Ranking de KDA obtenido de la View Vista_Resumen_Jugadores"""
    statement = select(Vista_Resumen_Jugadores)
    return session.exec(statement).all()

@app.get("/equipos/estadisticas", response_model=List[Vista_Estadisticas_Equipos])
def obtener_estadisticas_equipos(session: Session = Depends(get_session)):
    """Retorna las victorias y derrotas acumuladas desde Vista_Estadisticas_Equipos"""
    statement = select(Vista_Estadisticas_Equipos)
    return session.exec(statement).all()

# ==========================================
# 👥 ENDPOINTS PARA TABLAS Y AUDITORÍA (03-triggers.sql)
# ==========================================

@app.get("/jugadores", response_model=List[Jugador])
def listar_jugadores(session: Session = Depends(get_session)):
    """Trae la lista de jugadores de la tabla física"""
    statement = select(Jugador)
    return session.exec(statement).all()

@app.post("/jugadores", response_model=Jugador, status_code=status.HTTP_201_CREATED)
def crear_jugador(jugador_in: JugadorCreate, session: Session = Depends(get_session)):
    """
    Inserta un Jugador. Al ejecutarse, PostgreSQL disparará de manera 
    automática el trigger 'trg_auditoria_jugador' poblando la tabla Audit_Log.
    """
    db_jugador = Jugador.model_validate(jugador_in)
    session.add(db_jugador)
    session.commit()
    session.refresh(db_jugador)
    return db_jugador

@app.get("/auditoria", response_model=List[Audit_Log])
def ver_logs_auditoria(session: Session = Depends(get_session)):
    """Permite visualizar en el frontend los cambios capturados por tus Triggers"""
    statement = select(Audit_Log).order_by(text("Id_Audit DESC"))
    return session.exec(statement).all()


# ==========================================
# ⚡ ENDPOINT PARA PROCEDIMIENTOS ALMACENADOS (02-procedures.sql)
# ==========================================
@app.post("/partidas/registrar")
def registrar_partida_completa(datos: ProcedimientoPartidaInput):
    # Definimos la consulta plana con la sintaxis nativa de parámetros (%s)
    query = """
        CALL sp_registrar_partida(%s, %s, %s, %s, %s, %s, %s, %s, CAST(%s AS TIME));
    """
    
    # Extraemos el diccionario con los datos del JSON
    p = datos.model_dump()
    valores = (
        p["p_id_partida"],
        p["p_fase"],
        p["p_id_torneo"],
        p["p_id_mapa"],
        p["p_id_equipo1"],
        p["p_id_equipo2"],
        p["p_score1"],
        p["p_score2"],
        p["p_duracion"]
    )
    
    # 1. Accedemos al objeto de conexión crudo de la base de datos (DBAPI nativo)
    raw_connection = engine.raw_connection()
    raw_connection.autocommit = True  # Mantiene el driver libre de subtransacciones
    
    try:
        # 2. Creamos un cursor nativo
        with raw_connection.cursor() as cursor:
            # 3. Ejecutamos el CALL directo
            cursor.execute(query, valores)
            
        # 🚀 EL CAMBIO CLAVE: Obligamos a la conexión cruda a guardar físicamente en el disco
        raw_connection.commit()
            
        return {
            "status": "success", 
            "message": f"Procedimiento ejecutado. Partida {datos.p_id_partida} registrada con éxito."
        }
    finally:
        # 4. Cerramos la conexión manual para evitar fugas en el pool
        raw_connection.close()