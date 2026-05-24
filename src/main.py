import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, text  # 'text' ya está incluido aquí para evitar errores
from typing import List
from database import engine, get_session
from pydantic import BaseModel

# Importaciones directas y limpias sin prefijos molestos
from database import get_session
from models import (
    Vista_Resumen_Jugadores,
    Vista_Estadisticas_Equipos,
    Jugador,
    JugadorCreate,
    Audit_Log,
    ProcedimientoPartidaInput,
    Usuario,
    Equipo,
    Torneo
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

@app.post("/auth/register", tags=["Autenticación"])
def registrar_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    # Verificar si ya existe el username
    statement = select(Usuario).where(Usuario.username == usuario.username)
    db_user = session.exec(statement).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return {"message": "Usuario creado con éxito", "usuario": usuario.username}
# Modelo para recibir el JSON del frontend
class LoginRequest(BaseModel):
    username: str
    password_hash: str

@app.post("/auth/login", tags=["Autenticación"])
def login(request_data: LoginRequest, session: Session = Depends(get_session)):
    # Ahora extraemos los datos del objeto request_data
    statement = select(Usuario).where(Usuario.username == request_data.username)
    usuario = session.exec(statement).first()
    
    if not usuario or usuario.password_hash != request_data.password_hash:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
    return {
        "status": "Login exitoso",
        "username": usuario.username,
        "privilegios": usuario.rol_usuario
    }

# ==============================================================================
# ENDPOINTS PARA JUGADORES
# ==============================================================================
@app.put("/jugadores/{id_player}", tags=["Jugadores"])
def modificar_jugador(id_player: str, jugador_update: Jugador, session: Session = Depends(get_session)):
    db_jugador = session.get(Jugador, id_player)
    if not db_jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    
    # Actualizamos los campos recibidos
    db_jugador.nombre = jugador_update.nombre
    db_jugador.pais = jugador_update.pais
    db_jugador.agente = jugador_update.agente
    db_jugador.id_equipo = jugador_update.id_equipo
    
    session.add(db_jugador)
    session.commit()
    session.refresh(db_jugador)
    return {"message": "Jugador modificado exitosamente", "jugador": db_jugador}

# ==============================================================================
# ENDPOINTS PARA EQUIPOS (Creación y Modificación)
# ==============================================================================
@app.post("/equipos", tags=["Equipos"])
def crear_equipo(equipo: Equipo, session: Session = Depends(get_session)):
    # Al tener el ID automático, Postgres se encarga del prefijo 'E'
    session.add(equipo)
    session.commit()
    session.refresh(equipo)
    return {"message": "Equipo creado con éxito", "equipo": equipo}

@app.put("/equipos/{id_equipo}", tags=["Equipos"])
def modificar_equipo(id_equipo: str, equipo_update: Equipo, session: Session = Depends(get_session)):
    db_equipo = session.get(Equipo, id_equipo)
    if not db_equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
        
    db_equipo.nombre_equipo = equipo_update.nombre_equipo
    db_equipo.coach = equipo_update.coach
    db_equipo.region = equipo_update.region
    
    session.add(db_equipo)
    session.commit()
    session.refresh(db_equipo)
    return {"message": "Equipo modificado exitosamente", "equipo": db_equipo}

@app.get("/equipos", tags=["Equipos"])
def listar_equipos(session: Session = Depends(get_session)):
    """Trae la lista de todos los equipos formateados para el frontend"""
    try:
        query = text("SELECT id_equipo, nombre_equipo, region, coach FROM equipo;")
        result = session.execute(query).fetchall()
        return [
            {
                "id_equipo": str(r[0]),
                "nombre": r[1], 
                "region": r[2],
                "coach": r[3]
            }
            for r in result
        ]
    except Exception as e:
        print(f"❌ ERROR CRÍTICO EN EQUIPOS: {e}")
        raise HTTPException(status_code=500, detail=str(e))
# ==============================================================================
# ENDPOINTS PARA TORNEOS
# ==============================================================================
@app.put("/torneos/{id_torneo}", tags=["Torneos"])
def modificar_torneo(id_torneo: str, torneo_update: Torneo, session: Session = Depends(get_session)):
    db_torneo = session.get(Torneo, id_torneo)
    if not db_torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
        
    db_torneo.nombre_torneo = torneo_update.nombre_torneo
    db_torneo.region = torneo_update.region
    db_torneo.fecha_inicio = torneo_update.fecha_inicio
    db_torneo.fecha_fin = torneo_update.fecha_fin
    db_torneo.ubicacion = torneo_update.ubicacion
    db_torneo.premio_total = torneo_update.premio_total
    
    session.add(db_torneo)
    session.commit()
    session.refresh(db_torneo)
    return {"message": "Torneo modificado exitosamente", "torneo": db_torneo}

@app.get("/torneos", tags=["Torneos"])
def listar_torneos(session: Session = Depends(get_session)):
    """Trae la lista de todos los torneos formateados para el frontend"""
    try:
        query = text("""
            SELECT id_torneo, nombre_torneo, EXTRACT(YEAR FROM fecha_inicio) as anio, region 
            FROM torneo;
        """)
        result = session.execute(query).fetchall()
        
        return [
            {
                "id_torneo": str(r[0]),
                "nombre": r[1],
                "anio": int(r[2]) if r[2] is not None else 2026, 
                "region": r[3] if r[3] else "Global"
            }
            for r in result
        ]
    except Exception as e:
        print(f"❌ ERROR CRÍTICO EN TORNEOS: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/leaderboard", tags=["Valorant Tracker - Insights"])
def obtener_leaderboard(session: Session = Depends(get_session)):
    # SQL nativo rápido para agrupar y calcular el KDR acumulado de cada jugador
    query = """
        SELECT j.Nombre, e.id_equipofk, SUM(ej.kills) as total_kills, SUM(ej.death) as total_deaths,
               ROUND(SUM(ej.kills)::numeric / NULLIF(SUM(ej.death), 0), 2) as kdr
        FROM estadistica_jugador ej
        JOIN jugador j ON ej.id_playerfk = j.id_player
        GROUP BY j.Nombre, e.id_equipofk
        ORDER BY kdr DESC;
    """
    result = session.execute(text(query)).fetchall()
    
    # Formateamos la respuesta para que se vea estético en Swagger
    return [
        {"jugador": r[0], "equipo": r[1], "total_kills": r[2], "total_deaths": r[3], "kdr": r[4]}
        for r in result
    ]

@app.get("/analytics/equipos/{id_equipo}/map-stats", tags=["Valorant Tracker - Insights"])
def stats_mapas_equipo(id_equipo: str, session: Session = Depends(get_session)):
    query = """
        SELECT m.Nombre_Mapa, 
               COUNT(pe.id_partidafk) as partidas_jugadas,
               COUNT(CASE WHEN pe.indicador_victoria = TRUE THEN 1 END) as victorias,
               ROUND((COUNT(CASE WHEN pe.indicador_victoria = TRUE THEN 1 END)::numeric / COUNT(pe.id_partidafk)) * 100, 1) as winrate
        FROM partido_equipo pe
        JOIN estadistica_partida ep ON pe.id_partidafk = ep.id_partidafk
        JOIN mapa m ON ep.id_mapafk = m.id_mapa
        WHERE pe.id_equipofk = :id_equipo
        GROUP BY m.Nombre_Mapa;
    """
    result = session.execute(text(query), {"id_equipo": id_equipo}).fetchall()
    return [
        {"mapa": r[0], "jugadas": r[1], "victorias": r[2], "winrate_porcentaje": f"{r[3]}%"}
        for r in result
    ]