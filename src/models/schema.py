from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date, datetime


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
    __tablename__ = "equipo"
    id_equipo: Optional[str] = Field(default=None, primary_key=True)
    nombre_equipo: str
    coach: Optional[str] = None
    region: Optional[str] = None
    ultima_modificacion: Optional[datetime] = None


class Torneo(SQLModel, table=True):
    __tablename__ = "torneo"
    id_torneo: str = Field(primary_key=True)
    nombre_torneo: str
    region: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    ubicacion: Optional[str] = None
    premio_total: Optional[int] = None
    ultima_modificacion: Optional[datetime] = None


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
    ultima_modificacion: Optional[datetime] = None


class Jugador(SQLModel, table=True):
    __tablename__ = "jugador"
    id_player: str = Field(primary_key=True)
    nombre: str
    pais: Optional[str] = None
    agente: Optional[str] = None
    id_equipo: Optional[str] = None
    ultima_modificacion: Optional[datetime] = None


class Partido_Equipo(SQLModel, table=True):
    __tablename__ = "Partido_Equipo"
    Id_PartidaFK: str = Field(primary_key=True, foreign_key="Partida.Id_Partida")
    Id_EquipoFK: str = Field(primary_key=True, foreign_key="equipo.id_equipo")
    Indicador_victoria: Optional[bool] = None


class Estadistica_Partida(SQLModel, table=True):
    __tablename__ = "Estadistica_Partida"
    ID_Estadistica: str = Field(primary_key=True)
    Puntuacion_equipo1: Optional[int] = None
    Puntuacion_equipo2: Optional[int] = None
    Duracion: Optional[str] = None
    Id_PartidaFK: Optional[str] = Field(default=None, foreign_key="Partida.Id_Partida")
    Id_MapaFK: Optional[str] = Field(default=None, foreign_key="Mapa.Id_Mapa")


class Estadistica_Jugador(SQLModel, table=True):
    __tablename__ = "Estadistica_Jugador"
    Id_estadistica_jugador: str = Field(primary_key=True)
    kills: int = Field(default=0)
    death: int = Field(default=0)
    assists: int = Field(default=0)
    Id_PlayerFK: Optional[str] = Field(default=None, foreign_key="jugador.id_player")
    Id_AgenteFK: Optional[str] = Field(default=None, foreign_key="Agente.Id_Agente")
    Id_Partido: Optional[str] = Field(default=None, foreign_key="Partida.Id_Partida")


class Audit_Log(SQLModel, table=True):
    __tablename__ = "audit_log"
    id_audit: Optional[int] = Field(default=None, primary_key=True)
    tabla_afectada: str
    operacion: str
    usuario: str
    fecha_hora: datetime
    detalle: Optional[str] = Field(default=None)


class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"
    id_usuario: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
    rol_usuario: str = Field(default="Auditor")


class Vista_Resumen_Jugadores(SQLModel, table=True):
    __tablename__ = "vista_resumen_jugadores"
    jugador: str = Field(primary_key=True)
    equipo: str
    agente: str
    kills: int
    death: int
    assists: int
    kda: float


class Vista_Estadisticas_Equipos(SQLModel, table=True):
    __tablename__ = "vista_estadisticas_equipos"
    nombre_equipo: str = Field(primary_key=True)
    partidas_jugadas: int
    victorias: int
    derrotas: int


class Vista_Detalles_Partida(SQLModel, table=True):
    __tablename__ = "vista_detalles_partida"
    id_partida: str = Field(primary_key=True)
    torneo: str
    mapa: str
    fase: int
    fecha: date
    score_e1: int
    score_e2: int
    duracion: str
    equipo_1: str
    equipo_2: str
    ganador: str


class Vista_Meta_Agentes(SQLModel, table=True):
    __tablename__ = "vista_meta_agentes"
    nombre_agente: str = Field(primary_key=True)
    rol: str
    veces_elegido: int
    pick_rate: float
