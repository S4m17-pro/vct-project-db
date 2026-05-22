from typing import Optional
from sqlmodel import SQLModel, Field,Column, DateTime
from datetime import date,datetime

# ==========================================
# TABLAS INDEPENDIENTES (Nivel 1 - 00-schemas.sql)
# ==========================================
class Rol(SQLModel, table=True):
    __tablename__ = "Rol"
    Cod_Rol: str = Field(primary_key=True)
    Nombre_Rol: str

class Ultimate(SQLModel, table=True):
    __tablename__ = "Ultimate"
    Id_Ultimate: str = Field(primary_key=True)
    Nombre_Ultimate: str
    Dano: Optional[int] = None
    Puntos_de_ulti: Optional[int] = None
    Tiempo_de_activacion: Optional[float] = None

class Mapa(SQLModel, table=True):
    __tablename__ = "Mapa"
    Id_Mapa: str = Field(primary_key=True)
    Nombre_Mapa: str
    Ubicacion: Optional[str] = None
    Cantidad_Orbes: Optional[int] = None
    Cantidad_Sites: Optional[int] = None

class Equipo(SQLModel, table=True):
    __tablename__ = "Equipo"
    Id_Equipo: str = Field(primary_key=True)
    Nombre_Equipo: str
    Coach: Optional[str] = None
    Region: Optional[str] = None

class Torneo(SQLModel, table=True):
    __tablename__ = "Torneo"
    Id_Torneo: str = Field(primary_key=True)
    nombre_torneo: str
    Region: Optional[str] = None
    Fecha_inicio: Optional[date] = None
    Fecha_fin: Optional[date] = None
    Ubicacion: Optional[str] = None
    Premio_total: Optional[int] = None

class Arma(SQLModel, table=True):
    __tablename__ = "Arma"
    Id_Arma: str = Field(primary_key=True)
    Nombre_Arma: str
    Creditos: Optional[int] = None
    Tipo_de_arma: Optional[str] = None
    Tiempo_de_recarga: Optional[float] = None
    Balas_de_Cargador: Optional[int] = None
    Total_de_balas: Optional[int] = None
    Modo_de_disparo: Optional[str] = None

# ==========================================
# TABLAS CON DEPENDENCIAS (Nivel 2 - 00-schemas.sql)
# ==========================================

class Agente(SQLModel, table=True):
    __tablename__ = "Agente"
    Id_Agente: str = Field(primary_key=True)
    Nombre_Agente: str
    Rol: Optional[str] = Field(default=None, foreign_key="Rol.Cod_Rol")

class Habilidad(SQLModel, table=True):
    __tablename__ = "Habilidad"
    Id_Habilidad: str = Field(primary_key=True)
    Nombre_Habilidad: str
    Tecla: Optional[str] = None
    Dano: Optional[int] = None
    Cargas: Optional[int] = None
    Tiempo_de_activacion: Optional[float] = None
    Id_UltimateFK: Optional[str] = Field(default=None, foreign_key="Ultimate.Id_Ultimate")

class Partida(SQLModel, table=True):
    __tablename__ = "Partida"
    Id_Partida: str = Field(primary_key=True)
    fecha: Optional[date] = None
    Fase: Optional[int] = None
    Id_TorneoFK: Optional[str] = Field(default=None, foreign_key="Torneo.Id_Torneo")

class Jugador(SQLModel, table=True):
    __tablename__: str = "jugador"
    id_player: str = Field(primary_key=True, validation_alias="Id_Player")
    nombre: str = Field(validation_alias="Nombre")
    pais: str = Field(validation_alias="Pais")
    agente: str = Field(validation_alias="Agente")
    id_equipo: Optional[str] = Field(default=None, validation_alias="Id_Equipo")

# ==========================================
# TABLAS DE RELACIÓN Y ESTADÍSTICAS (Nivel 3 - 00-schemas.sql)
# ==========================================

class Partido_Equipo(SQLModel, table=True):
    __tablename__ = "Partido_Equipo"
    Id_PartidaFK: str = Field(primary_key=True, foreign_key="Partida.Id_Partida")
    Id_EquipoFK: str = Field(primary_key=True, foreign_key="Equipo.Id_Equipo")
    Indicador_victoria: Optional[bool] = None

class Estadistica_Partida(SQLModel, table=True):
    __tablename__ = "Estadistica_Partida"
    ID_Estadistica: str = Field(primary_key=True)
    Puntuacion_equipo1: Optional[int] = None
    Puntuacion_equipo2: Optional[int] = None
    Duracion: Optional[str] = None  # Mapeado como string para el tipo TIME de Postgres
    Id_PartidaFK: Optional[str] = Field(default=None, foreign_key="Partida.Id_Partida")
    Id_MapaFK: Optional[str] = Field(default=None, foreign_key="Mapa.Id_Mapa")

class Estadistica_Jugador(SQLModel, table=True):
    __tablename__ = "Estadistica_Jugador"
    Id_estadistica_jugador: str = Field(primary_key=True)
    kills: int = Field(default=0)
    death: int = Field(default=0)
    assists: int = Field(default=0)
    Id_PlayerFK: Optional[str] = Field(default=None, foreign_key="Jugador.Id_Player")
    Id_AgenteFK: Optional[str] = Field(default=None, foreign_key="Agente.Id_Agente")
    Id_Partido: Optional[str] = Field(default=None, foreign_key="Partida.Id_Partida")

class Audit_Log(SQLModel, table=True):
    __tablename__: str = "audit_log"
    id_audit: Optional[int] = Field(default=None, primary_key=True)
    tabla_afectada: str
    operacion: str
    usuario: str
    fecha_hora: datetime = Field(sa_column=Column(DateTime(timezone=False)))
    detalle: Optional[str] = Field(default=None)
# ==========================================
# MODELOS PARA LAS VISTAS (01-views.sql)
# ==========================================

class Vista_Resumen_Jugadores(SQLModel, table=True):
    __tablename__ = "vista_resumen_jugadores"
    
    # Todo en minúsculas exactas como te lo mostró el information_schema
    jugador: str = Field(primary_key=True)  
    equipo: str
    agente: str
    kills: int
    death: int
    assists: int
    kda: float

class Vista_Estadisticas_Equipos(SQLModel, table=True):
    __tablename__ = "vista_estadisticas_equipos"
    
    # Asumiendo que tu otra vista sigue el mismo patrón estándar de Postgres
    nombre_equipo: str = Field(primary_key=True)
    partidas_jugadas: int
    victorias: int
    derrotas: int
# ==========================================
# SCHEMAS DE VALIDACIÓN (DTOs para Inputs desde Web)
# ==========================================

class JugadorCreate(SQLModel):
    Id_Player: str
    Nombre: str
    Pais: Optional[str] = None
    Agente: Optional[str] = None
    Id_Equipo: Optional[str] = None

class ProcedimientoPartidaInput(SQLModel):
    p_id_partida: str
    p_fase: int
    p_id_torneo: str
    p_id_mapa: str
    p_id_equipo1: str
    p_id_equipo2: str
    p_score1: int
    p_score2: int
    p_duracion: str  # Ejemplo: "00:45:00"