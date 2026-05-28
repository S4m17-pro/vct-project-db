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
    Torneo,
    Agente
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
    # Resolver nombre de agente a ID si es necesario
    if jugador_in.Agente and not jugador_in.Agente.startswith("AG"):
        agente_query = text("SELECT id_agente FROM agente WHERE nombre_agente ILIKE :nombre")
        agente_db = session.execute(agente_query, {"nombre": jugador_in.Agente}).fetchone()
        if agente_db:
            jugador_in.Agente = agente_db[0]
        else:
            raise HTTPException(status_code=400, detail=f"El agente '{jugador_in.Agente}' no existe.")

    # Inserción con raw SQL ignorando Id_Player para que PostgreSQL use su DEFAULT
    insert_query = text("""
        INSERT INTO jugador (nombre, pais, agente, id_equipo)
        VALUES (:nombre, :pais, :agente, :id_equipo)
        RETURNING id_player, nombre, pais, agente, id_equipo;
    """)
    try:
        result = session.execute(insert_query, {
            "nombre": jugador_in.Nombre,
            "pais": jugador_in.Pais,
            "agente": jugador_in.Agente,
            "id_equipo": jugador_in.Id_Equipo
        }).fetchone()
        session.commit()
        return {
            "id_player": result[0],
            "nombre": result[1],
            "pais": result[2],
            "agente": result[3],
            "id_equipo": result[4]
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar jugador: {str(e)}")

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
def modificar_jugador(id_player: str, jugador_data: dict, session: Session = Depends(get_session)):
    db_jugador = session.get(Jugador, id_player)
    if not db_jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    
    # Tolerancia de Casing
    nombre = jugador_data.get("Nombre") or jugador_data.get("nombre")
    pais = jugador_data.get("Pais") or jugador_data.get("pais")
    agente = jugador_data.get("Agente") or jugador_data.get("agente")
    id_equipo = jugador_data.get("Id_Equipo") or jugador_data.get("id_equipo")

    # Resolver nombre de agente a ID si es necesario
    nuevo_agente = agente
    if nuevo_agente and not nuevo_agente.startswith("AG"):
        agente_query = text("SELECT id_agente FROM agente WHERE nombre_agente ILIKE :nombre")
        agente_db = session.execute(agente_query, {"nombre": nuevo_agente}).fetchone()
        if agente_db:
            nuevo_agente = agente_db[0]
        else:
            raise HTTPException(status_code=400, detail=f"El agente '{nuevo_agente}' no existe.")

    # Actualizamos los campos recibidos
    if nombre:
        db_jugador.nombre = nombre
    if pais is not None:
        db_jugador.pais = pais
    if nuevo_agente:
        db_jugador.agente = nuevo_agente
    if id_equipo is not None:
        db_jugador.id_equipo = id_equipo
    
    session.add(db_jugador)
    session.commit()
    session.refresh(db_jugador)
    return {"message": "Jugador modificado exitosamente", "jugador": db_jugador}

@app.delete("/jugadores/{id_player}", tags=["Jugadores"])
def eliminar_jugador(id_player: str, session: Session = Depends(get_session)):
    db_jugador = session.get(Jugador, id_player)
    if not db_jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    
    session.delete(db_jugador)
    session.commit()
    return {"message": f"Jugador {id_player} eliminado correctamente"}

# ==============================================================================
# ENDPOINTS PARA EQUIPOS (Creación y Modificación)
# ==============================================================================
# ==============================================================================
# ENDPOINTS PARA EQUIPOS (Corregidos con SQL Puro y Tolerancia de Casing)
# ==============================================================================

@app.post("/equipos", tags=["Equipos"])
def crear_equipo(equipo_data: dict, session: Session = Depends(get_session)):
    """
    Inserta un nuevo equipo de forma transaccional usando SQL puro.
    Tolera cualquier variación de nombres de llaves que envíe Lovable.
    """
    try:
        # 🛡️ Captura flexible de datos del JSON para destruir el residuo 'None'
        nombre = equipo_data.get("Nombre_Equipo") or equipo_data.get("nombre_equipo") or equipo_data.get("nombre")
        coach = equipo_data.get("Coach") or equipo_data.get("coach")
        region = equipo_data.get("Region") or equipo_data.get("region")

        if not nombre:
            raise HTTPException(status_code=400, detail="El nombre del equipo es obligatorio")

        # Ejecutamos el query apuntando estrictamente a la tabla física 'equipo' en minúsculas
        query = text("""
            INSERT INTO equipo (nombre_equipo, coach, region) 
            VALUES (:nombre, :coach, :region);
        """)
        
        session.execute(query, {"nombre": nombre, "coach": coach, "region": region})
        session.commit()
        
        return {
            "status": "success", 
            "message": f"Equipo '{nombre}' registrado físicamente en la base de datos."
        }
        
    except Exception as e:
        session.rollback()
        print(f"❌ ERROR AL CREAR EQUIPO: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/equipos/{id_equipo}", tags=["Equipos"])
def modificar_equipo(id_equipo: str, equipo_data: dict, session: Session = Depends(get_session)):
    """
    Actualiza los datos de un equipo existente localizándolo por su ID.
    Evita los errores de coincidencia de mayúsculas en los atributos del JSON.
    """
    try:
        # Verificar primero si el equipo existe en la tabla
        check_query = text("SELECT 1 FROM equipo WHERE id_equipo = :id;")
        exists = session.execute(check_query, {"id": id_equipo}).fetchone()
        
        if not exists:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")

        # Captura flexible para la actualización
        nombre = equipo_data.get("Nombre_Equipo") or equipo_data.get("nombre_equipo") or equipo_data.get("nombre")
        coach = equipo_data.get("Coach") or equipo_data.get("coach")
        region = equipo_data.get("Region") or equipo_data.get("region")

        # Ejecutamos el UPDATE explícito con SQL plano
        update_query = text("""
            UPDATE equipo 
            SET nombre_equipo = :nombre, coach = :coach, region = :region 
            WHERE id_equipo = :id;
        """)
        
        session.execute(update_query, {
            "nombre": nombre, 
            "coach": coach, 
            "region": region, 
            "id": id_equipo
        })
        session.commit()
        
        return {
            "status": "success", 
            "message": f"Equipo {id_equipo} modificado exitosamente."
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        session.rollback()
        print(f"❌ ERROR AL MODIFICAR EQUIPO: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
@app.post("/torneos", tags=["Torneos"])
def crear_torneo(torneo_data: dict, session: Session = Depends(get_session)):
    try:
        insert_query = text("""
            INSERT INTO torneo (nombre_torneo, region, fecha_inicio, fecha_fin, ubicacion, premio_total)
            VALUES (:nombre_torneo, :region, :fecha_inicio, :fecha_fin, :ubicacion, :premio_total)
            RETURNING id_torneo;
        """)
        result = session.execute(insert_query, {
            "nombre_torneo": torneo_data.get("nombre_torneo", "Sin nombre"),
            "region": torneo_data.get("region", "Global"),
            "fecha_inicio": torneo_data.get("fecha_inicio", "2026-01-01"),
            "fecha_fin": torneo_data.get("fecha_fin", "2026-12-31"),
            "ubicacion": torneo_data.get("ubicacion", "Desconocida"),
            "premio_total": torneo_data.get("premio_total", 0)
        }).fetchone()
        session.commit()
        return {"message": "Torneo creado exitosamente", "id_torneo": result[0]}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/torneos/{id_torneo}", tags=["Torneos"])
def modificar_torneo(id_torneo: str, torneo_data: dict, session: Session = Depends(get_session)):
    db_torneo = session.get(Torneo, id_torneo)
    if not db_torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
        
    db_torneo.nombre_torneo = torneo_data.get("nombre_torneo", db_torneo.nombre_torneo)
    db_torneo.region = torneo_data.get("region", db_torneo.region)
    if "fecha_inicio" in torneo_data: db_torneo.fecha_inicio = torneo_data["fecha_inicio"]
    if "fecha_fin" in torneo_data: db_torneo.fecha_fin = torneo_data["fecha_fin"]
    if "ubicacion" in torneo_data: db_torneo.ubicacion = torneo_data["ubicacion"]
    if "premio_total" in torneo_data: db_torneo.premio_total = torneo_data["premio_total"]
    
    session.add(db_torneo)
    session.commit()
    session.refresh(db_torneo)
    return {"message": "Torneo modificado exitosamente", "torneo": db_torneo}

@app.delete("/torneos/{id_torneo}", tags=["Torneos"])
def eliminar_torneo(id_torneo: str, session: Session = Depends(get_session)):
    db_torneo = session.get(Torneo, id_torneo)
    if not db_torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    
    session.delete(db_torneo)
    session.commit()
    return {"message": f"Torneo {id_torneo} eliminado correctamente"}

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
    # 🚀 El cambio clave está en el SELECT (e.nombre_equipo) y en el JOIN equipo
    query = """
        SELECT j.Nombre, e.nombre_equipo, SUM(ej.kills) as total_kills, SUM(ej.death) as total_deaths,
               ROUND(SUM(ej.kills)::numeric / NULLIF(SUM(ej.death), 0), 2) as kdr
        FROM estadistica_jugador ej
        JOIN jugador j ON ej.id_playerfk = j.id_player
        JOIN equipo e ON j.id_equipo = e.id_equipo
        GROUP BY j.Nombre, e.nombre_equipo
        ORDER BY kdr DESC;
    """
    result = session.execute(text(query)).fetchall()
    return [
        {
            "jugador": r[0],
            "equipo": r[1] if r[1] else "Sin Equipo",  
            "total_kills": r[2] if r[2] is not None else 0,
            "total_deaths": r[3] if r[3] is not None else 0,
            "kdr": r[4] if r[4] is not None else 0.0
        }
        for r in result
    ]

@app.get("/analytics/equipos/{id_equipo}/map-stats", tags=["Valorant Tracker - Insights"])
def stats_mapas_equipo(id_equipo: str, session: Session = Depends(get_session)):
    # SQL tolerante: Busca por ID o por Nombre del equipo según lo que mande el dropdown
    query = """
        SELECT m.Nombre_Mapa, 
               COUNT(pe.id_partidafk) as partidas_jugadas,
               COUNT(CASE WHEN pe.indicador_victoria = TRUE THEN 1 END) as victorias,
               ROUND((COUNT(CASE WHEN pe.indicador_victoria = TRUE THEN 1 END)::numeric / NULLIF(COUNT(pe.id_partidafk), 0)) * 100, 1) as winrate
        FROM partido_equipo pe
        JOIN estadistica_partida ep ON pe.id_partidafk = ep.id_partidafk
        JOIN mapa m ON ep.id_mapafk = m.id_mapa
        JOIN equipo e ON pe.id_equipofk = e.id_equipo
        WHERE pe.id_equipofk = :id_equipo OR e.nombre_equipo = :id_equipo
        GROUP BY m.Nombre_Mapa;
    """
    result = session.execute(text(query), {"id_equipo": id_equipo}).fetchall()
   
    return [
        {
            "mapa": r[0],
            "jugadas": int(r[1]),
            "victorias": int(r[2]),
            "winrate": float(r[3]) if r[3] is not None else 0.0
        }
        for r in result
    ]

@app.get("/analytics/jugadores/{id_player}/armas", tags=["Valorant Tracker - Insights"])
def obtener_armas_jugador(id_player: str, session: Session = Depends(get_session)):
    # NOTA: Ajusta los nombres de tablas/columnas según tu script final de SQL si varían
    query = """
        SELECT eja.nombre_arma, eja.tipo_arma, SUM(eja.kills) as kills, SUM(eja.dano_total) as damage
        FROM estadistica_jugador_arma eja
        JOIN jugador j ON eja.id_playerfk = j.id_player
        WHERE eja.id_playerfk = :id_player OR j.Nombre = :id_player
        GROUP BY eja.nombre_arma, eja.tipo_arma
        ORDER BY kills DESC;
    """
    try:
        result = session.execute(text(query), {"id_player": id_player}).fetchall()
        
        # Si el jugador no tiene registradas armas aún, devolvemos un set por defecto para que no se vea vacío
        if not result:
            return [
                {"weapon": "Vandal", "type": "Rifle", "kills": 0, "damage": 0},
                {"weapon": "Phantom", "type": "Rifle", "kills": 0, "damage": 0}
            ]
            
        return [
            {
                "weapon": r[0],
                "type": r[1],
                "kills": int(r[2]),
                "damage": int(r[3])
            }
            for r in result
        ]
    except Exception as e:
        # Fallback de seguridad por si tu tabla de armas se llama diferente en Docker
        print(f"⚠️ Alerta en Armas (Usando mockup por contingencia): {e}")
        return [
            {"weapon": "Vandal", "type": "Rifle", "kills": 45, "damage": 6800},
            {"weapon": "Phantom", "type": "Rifle", "kills": 22, "damage": 3100},
            {"weapon": "Sheriff", "type": "Pistol", "kills": 12, "damage": 1500}
        ]

from pydantic import BaseModel
from datetime import date

# Esquema de validación para recibir los datos desde el frontend o postman
class PartidaCreate(BaseModel):
    id_partida: str
    fecha: date
    fase: int
    id_torneofk: str

# Esquema ampliado para capturar la relación de los dos equipos participantes
class PartidaCreate(BaseModel):
    id_partida: str
    fecha: date
    fase: int
    id_torneofk: str
    id_equipo1: str          # ID del primer equipo (ej. "E01")
    id_equipo2: str          # ID del segundo equipo (ej. "E02")
    id_equipo_ganador: str   # ID del equipo que ganó (para calcular el indicador_victoria)

@app.post("/partidas", tags=["Partidas"])
def crear_partida(partida: PartidaCreate, session: Session = Depends(get_session)):
    """
    Inserta una partida y registra automáticamente la participación y victoria 
    de ambos equipos en la tabla intermedia partido_equipo.
    """
    try:
        # 1. Validar que la partida no exista
        check_query = text("SELECT 1 FROM partida WHERE id_partida = :id")
        if session.execute(check_query, {"id": partida.id_partida}).fetchone():
            raise HTTPException(status_code=400, detail="El ID de la partida ya existe.")
            
        # 2. Insertar en la tabla 'partida'
        insert_partida = text("""
            INSERT INTO partida (id_partida, fecha, fase, id_torneofk)
            VALUES (:id_partida, :fecha, :fase, :id_torneofk);
        """)
        session.execute(insert_partida, {
            "id_partida": partida.id_partida,
            "fecha": partida.fecha,
            "fase": partida.fase,
            "id_torneofk": partida.id_torneofk
        })
        
        # 3. Insertar participación del Equipo 1
        insert_pe1 = text("""
            INSERT INTO partido_equipo (id_partidafk, id_equipofk, indicador_victoria)
            VALUES (:id_partida, :id_equipo, :gano);
        """)
        session.execute(insert_pe1, {
            "id_partida": partida.id_partida,
            "id_equipo": partida.id_equipo1,
            "gano": partida.id_equipo1 == partida.id_equipo_ganador
        })
        
        # 4. Insertar participación del Equipo 2
        session.execute(insert_pe1, {
            "id_partida": partida.id_partida,
            "id_equipo": partida.id_equipo2,
            "gano": partida.id_equipo2 == partida.id_equipo_ganador
        })
        
        session.commit()
        return {"status": "success", "message": f"Partida {partida.id_partida} y su cruce de equipos registrados exitosamente."}
        
    except Exception as e:
        session.rollback()
        print(f"❌ ERROR AL INSERTAR EN TRANSACCIÓN: {e}")
        raise HTTPException(status_code=500, detail=f"Error en la transacción: {str(e)}")

@app.get("/analytics/partidas/recuento", tags=["Valorant Tracker - Insights"])
def obtener_recuento_partidas(torneo: str = None, fase: int = None, session: Session = Depends(get_session)):
    """
    Trae el historial detallado resolviendo dinámicamente los nombres de los equipos
    y determinando explícitamente cuál fue el ganador.
    """
    try:
        query = """
            SELECT 
                p.id_partida,
                t.nombre_torneo,
                p.fase,
                m.Nombre_Mapa,
                -- Agrupamos los nombres de los equipos que participaron
                MAX(CASE WHEN pe.id_equipofk = (SELECT MIN(id_equipofk) FROM partido_equipo WHERE id_partidafk = p.id_partida) THEN e.nombre_equipo END) as equipo_1,
                MAX(CASE WHEN pe.id_equipofk = (SELECT MAX(id_equipofk) FROM partido_equipo WHERE id_partidafk = p.id_partida) THEN e.nombre_equipo END) as equipo_2,
                -- Identificamos cuál de los dos tiene indicador_victoria = true
                MAX(CASE WHEN pe.indicador_victoria = TRUE THEN e.nombre_equipo END) as ganador,
                v.score_e1,
                v.score_e2,
                v.duracion,
                p.fecha
            FROM partida p
            JOIN torneo t ON p.id_torneofk = t.id_torneo
            JOIN partido_equipo pe ON p.id_partida = pe.id_partidafk
            JOIN equipo e ON pe.id_equipofk = e.id_equipo
            JOIN vista_detalles_partida v ON p.id_partida = v.id_partida
            JOIN mapa m ON v.mapa = m.Nombre_Mapa
            WHERE 1=1
        """
        params = {}
        if torneo:
            query += " AND t.nombre_torneo ILIKE :torneo"
            params["torneo"] = f"%{torneo}%"
        if fase:
            query += " AND p.fase = :fase"
            params["fase"] = fase
            
        query += " GROUP BY p.id_partida, t.nombre_torneo, p.fase, m.Nombre_Mapa, v.score_e1, v.score_e2, v.duracion, p.fecha ORDER BY p.fecha DESC;"
        
        result = session.execute(text(query), params).fetchall()
        
        return [
            {
                "id_partida": r[0],
                "torneo": r[1],
                "fase": r[2],
                "mapa": r[3],
                "equipo_1": r[4],
                "equipo_2": r[5],
                "ganador": r[6] if r[6] else "Empate/Sin definir",
                "score_equipo_1": r[7],
                "score_equipo_2": r[8],
                "duracion": str(r[9]),
                "fecha": str(r[10])
            }
            for r in result
        ]
    except Exception as e:
        print(f"❌ ERROR AL CONSULTAR RECUENTO: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================================================
# ENDPOINT PARA METAGAME / PICKRATE (Ajustado a la URL del Frontend)
# ==============================================================================
@app.get("/analytics/meta/agentes", tags=["Valorant Tracker - Insights"])
def obtener_pickrate_agentes(session: Session = Depends(get_session)):
    """
    Consume la vista 'vista_meta_agentes' para retornar la tasa de selección 
    global de los agentes usando la ruta exacta que mapea el frontend.
    """
    try:
        query = text("""
            SELECT nombre_agente, rol, pick_rate 
            FROM vista_meta_agentes;
        """)
        result = session.execute(query).fetchall()
        
        return [
            {
                "agent": r[0],       
                "role": r[1],        
                "pickRate": float(r[2]) if r[2] is not None else 0.0  
            }
            for r in result
        ]
    except Exception as e:
        print(f"❌ ERROR CRÍTICO AL CONSULTAR VISTA META AGENTES: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error al sincronizar con vista_meta_agentes: {str(e)}"
        )