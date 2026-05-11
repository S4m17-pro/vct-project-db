-- Creación de Roles/Usuarios
-- Nota: En Docker/Postgres, los roles se crean a nivel de instancia
CREATE USER usuario_consulta WITH PASSWORD 'consulta123';
CREATE USER usuario_editor WITH PASSWORD 'editor123';

-- 1. Privilegios para el Consultor (Solo Lectura)
-- Le permitimos conectarse a la base de datos
GRANT CONNECT ON DATABASE vct_stats TO usuario_consulta;
-- Le damos permiso para ver las tablas en el esquema público
GRANT USAGE ON SCHEMA public TO usuario_consulta;
-- Solo puede hacer SELECT en todas las tablas actuales
GRANT SELECT ON ALL TABLES IN SCHEMA public TO usuario_consulta;

-- 2. Privilegios para el Editor (CRUD)
GRANT CONNECT ON DATABASE vct_stats TO usuario_editor;
GRANT USAGE ON SCHEMA public TO usuario_editor;
-- Puede leer, insertar, actualizar y borrar datos
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO usuario_editor;
-- Importante: darle permisos sobre las secuencias (para los IDs autoincrementales)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO usuario_editor;

-- 1. Tablas Independientes (Nivel 1)
CREATE TABLE Rol (
    Cod_Rol VARCHAR(10) PRIMARY KEY,
    Nombre_Rol VARCHAR(50) NOT NULL
);

CREATE TABLE Ultimate (
    Id_Ultimate VARCHAR(10) PRIMARY KEY,
    Nombre_Ultimate VARCHAR(60) NOT NULL,
    Dano INTEGER,
    Puntos_de_ulti INTEGER,
    Tiempo_de_activacion FLOAT
);

CREATE TABLE Mapa (
    Id_Mapa VARCHAR(10) PRIMARY KEY,
    Nombre_Mapa VARCHAR(30) NOT NULL,
    Ubicacion VARCHAR(50),
    Cantidad_Orbes INTEGER,
    Cantidad_Sites INTEGER
);

CREATE TABLE Equipo (
    Id_Equipo VARCHAR(10) PRIMARY KEY,
    Nombre_Equipo VARCHAR(50) NOT NULL,
    Coach VARCHAR(50),
    Region VARCHAR(50)
);

CREATE TABLE Torneo (
    Id_Torneo VARCHAR(10) PRIMARY KEY,
    nombre_torneo VARCHAR(50) NOT NULL,
    Region VARCHAR(50),
    Fecha_inicio DATE,
    Fecha_fin DATE,
    Ubicacion VARCHAR(50),
    Premio_total BIGINT
);

CREATE TABLE Arma (
    Id_Arma VARCHAR(10) PRIMARY KEY,
    Nombre_Arma VARCHAR(30) NOT NULL,
    Creditos INTEGER,
    Tipo_de_arma VARCHAR(30),
    Tiempo_de_recarga FLOAT,
    Balas_de_Cargador INTEGER,
    Total_de_balas INTEGER,
    Modo_de_disparo VARCHAR(30)
);

-- 2. Tablas con Dependencias (Nivel 2)
CREATE TABLE Agente (
    Id_Agente VARCHAR(10) PRIMARY KEY,
    Nombre_Agente VARCHAR(30) NOT NULL,
    Rol VARCHAR(10) REFERENCES Rol(Cod_Rol)
);

CREATE TABLE Habilidad (
    Id_Habilidad VARCHAR(10) PRIMARY KEY,
    Nombre_Habilidad VARCHAR(60) NOT NULL,
    Tecla VARCHAR(1),
    Dano INTEGER,
    Cargas INTEGER,
    Tiempo_de_activacion FLOAT,
    Id_UltimateFK VARCHAR(10) REFERENCES Ultimate(Id_Ultimate)
);

CREATE TABLE Partida (
    Id_Partida VARCHAR(10) PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    Fase INTEGER,
    Id_TorneoFK VARCHAR(10) REFERENCES Torneo(Id_Torneo)
);

CREATE TABLE Jugador (
    Id_Player VARCHAR(10) PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Pais VARCHAR(50),
    Agente VARCHAR(10) REFERENCES Agente(Id_Agente),
    Id_Equipo VARCHAR(10) REFERENCES Equipo(Id_Equipo)
);

-- 3. Tablas de Relación y Estadísticas (Nivel 3)
CREATE TABLE Agente_Habilidad (
    Id_AgenteFK VARCHAR(10) REFERENCES Agente(Id_Agente),
    Id_HabilidadFK VARCHAR(10) REFERENCES Habilidad(Id_Habilidad),
    Orden_Habilidad INTEGER,
    PRIMARY KEY (Id_AgenteFK, Id_HabilidadFK)
);

CREATE TABLE Partido_Equipo (
    Id_PartidaFK VARCHAR(10) REFERENCES Partida(Id_Partida),
    Id_EquipoFK VARCHAR(10) REFERENCES Equipo(Id_Equipo),
    Indicador_victoria BOOLEAN,
    PRIMARY KEY (Id_PartidaFK, Id_EquipoFK)
);

CREATE TABLE Estadistica_Partida (
    ID_Estadistica VARCHAR(10) PRIMARY KEY,
    Puntuacion_equipo1 INTEGER,
    Puntuacion_equipo2 INTEGER,
    Duracion TIME,
    Id_PartidaFK VARCHAR(10) REFERENCES Partida(Id_Partida),
    Id_MapaFK VARCHAR(10) REFERENCES Mapa(Id_Mapa)
);

CREATE TABLE Estadistica_Jugador (
    Id_estadistica_jugador VARCHAR(10) PRIMARY KEY,
    kills INTEGER DEFAULT 0,
    death INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    Id_PlayerFK VARCHAR(10) REFERENCES Jugador(Id_Player),
    Id_AgenteFK VARCHAR(10) REFERENCES Agente(Id_Agente),
    Id_Partido VARCHAR(10) REFERENCES Partida(Id_Partida)
);

CREATE TABLE Uso_Armas_Jugador (
    Id_Uso_Arma VARCHAR(10) PRIMARY KEY,
    Id_estadistica_jugadorFK VARCHAR(10) REFERENCES Estadistica_Jugador(Id_estadistica_jugador),
    Id_ArmaFK VARCHAR(10) REFERENCES Arma(Id_Arma),
    Kills_con_arma INTEGER DEFAULT 0,
    Dano_con_arma INTEGER DEFAULT 0
);