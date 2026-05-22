-- Creación de Roles/Usuarios
-- Nota: En Docker/Postgres, los roles se crean a nivel de instancia
CREATE USER usuario_consulta WITH PASSWORD 'consulta123';
CREATE USER usuario_editor WITH PASSWORD 'editor123';

-- 1. Privilegios básicos para el Consultor
-- Le permitimos conectarse a la base de datos
GRANT CONNECT ON DATABASE vct_stats TO usuario_consulta;
GRANT USAGE ON SCHEMA public TO usuario_consulta;

-- 2. Privilegios básicos para el Editor
GRANT CONNECT ON DATABASE vct_stats TO usuario_editor;
GRANT USAGE ON SCHEMA public TO usuario_editor;

-- 3. Usuario Lewis (Colaborador)
-- Creamos a Lewis con permisos similares al editor para que pueda trabajar
CREATE USER lewis WITH PASSWORD 'lewis123';
GRANT CONNECT ON DATABASE vct_stats TO lewis;
GRANT USAGE ON SCHEMA public TO lewis;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO lewis;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO lewis;

-- Permisos para que Lewis pueda ver y ejecutar funciones/procedimientos futuros
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO lewis;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO lewis;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO lewis;
-- ==============================================================================
-- 0. CREACIÓN DE SECUENCIAS (Para automatizar los IDs de todas las tablas)
-- ==============================================================================
CREATE SEQUENCE sec_rol START WITH 5;          -- Ya tienes de R01 a R04
CREATE SEQUENCE sec_ultimate START WITH 29;     -- Ya tienes de U01 a U28
CREATE SEQUENCE sec_mapa START WITH 12;         -- Tienes hasta M11, inicia en M12
CREATE SEQUENCE sec_equipo START WITH 13;       -- Tienes hasta E12, inicia en E13
CREATE SEQUENCE sec_torneo START WITH 2;         -- Tienes T01
CREATE SEQUENCE sec_arma START WITH 4;           -- Tienes hasta A03
CREATE SEQUENCE sec_agente START WITH 29;       -- Tienes hasta AG28
CREATE SEQUENCE sec_habilidad START WITH 29;    -- Tienes hasta H28
CREATE SEQUENCE sec_partida START WITH 4;       -- Tienes hasta P03
CREATE SEQUENCE sec_jugador START WITH 11;       -- Tienes hasta J10, inicia en J11
CREATE SEQUENCE sec_est_partida START WITH 4;   -- Tienes hasta EP03
CREATE SEQUENCE sec_est_jugador START WITH 9;   -- Tienes hasta EJ08, inicia en EJ09
CREATE SEQUENCE sec_uso_arma START WITH 3;       -- Tienes hasta UA02

-- ==============================================================================
-- 1. TABLAS INDEPENDIENTES (Nivel 1)
-- ==============================================================================

CREATE TABLE Rol (
    Cod_Rol VARCHAR(10) PRIMARY KEY DEFAULT ('R' || lpad(nextval('sec_rol')::text, 2, '0')),
    Nombre_Rol VARCHAR(50) NOT NULL
);

CREATE TABLE Ultimate (
    Id_Ultimate VARCHAR(10) PRIMARY KEY DEFAULT ('U' || lpad(nextval('sec_ultimate')::text, 2, '0')),
    Nombre_Ultimate VARCHAR(60) NOT NULL,
    Dano INTEGER,
    Puntos_de_ulti INTEGER,
    Tiempo_de_activacion FLOAT
);

CREATE TABLE Mapa (
    Id_Mapa VARCHAR(10) PRIMARY KEY DEFAULT ('M' || lpad(nextval('sec_mapa')::text, 2, '0')),
    Nombre_Mapa VARCHAR(30) NOT NULL,
    Ubicacion VARCHAR(50),
    Cantidad_Orbes INTEGER,
    Cantidad_Sites INTEGER
);

CREATE TABLE Equipo (
    Id_Equipo VARCHAR(10) PRIMARY KEY DEFAULT ('E' || lpad(nextval('sec_equipo')::text, 2, '0')),
    Nombre_Equipo VARCHAR(50) NOT NULL,
    Coach VARCHAR(50),
    Region VARCHAR(50)
);

CREATE TABLE Torneo (
    Id_Torneo VARCHAR(10) PRIMARY KEY DEFAULT ('T' || lpad(nextval('sec_torneo')::text, 2, '0')),
    nombre_torneo VARCHAR(50) NOT NULL,
    Region VARCHAR(50),
    Fecha_inicio DATE,
    Fecha_fin DATE,
    Ubicacion VARCHAR(50),
    Premio_total BIGINT
);

CREATE TABLE Arma (
    Id_Arma VARCHAR(10) PRIMARY KEY DEFAULT ('A' || lpad(nextval('sec_arma')::text, 2, '0')),
    Nombre_Arma VARCHAR(30) NOT NULL,
    Creditos INTEGER,
    Tipo_de_arma VARCHAR(30),
    Tiempo_de_recarga FLOAT,
    Balas_de_Cargador INTEGER,
    Total_de_balas INTEGER,
    Modo_de_disparo VARCHAR(30)
);

-- ==============================================================================
-- 2. TABLAS CON DEPENDENCIAS (Nivel 2)
-- ==============================================================================

CREATE TABLE Agente (
    Id_Agente VARCHAR(10) PRIMARY KEY DEFAULT ('AG' || lpad(nextval('sec_agente')::text, 2, '0')),
    Nombre_Agente VARCHAR(30) NOT NULL,
    Rol VARCHAR(10) REFERENCES Rol(Cod_Rol)
);

CREATE TABLE Habilidad (
    Id_Habilidad VARCHAR(10) PRIMARY KEY DEFAULT ('H' || lpad(nextval('sec_habilidad')::text, 2, '0')),
    Nombre_Habilidad VARCHAR(60) NOT NULL,
    Tecla VARCHAR(1),
    Dano INTEGER,
    Cargas INTEGER,
    Tiempo_de_activacion FLOAT,
    Id_UltimateFK VARCHAR(10) REFERENCES Ultimate(Id_Ultimate)
);

CREATE TABLE Partida (
    Id_Partida VARCHAR(10) PRIMARY KEY DEFAULT ('P' || lpad(nextval('sec_partida')::text, 2, '0')),
    fecha DATE DEFAULT CURRENT_DATE,
    Fase INTEGER,
    Id_TorneoFK VARCHAR(10) REFERENCES Torneo(Id_Torneo)
);

CREATE TABLE Jugador (
    Id_Player VARCHAR(10) PRIMARY KEY DEFAULT ('J' || lpad(nextval('sec_jugador')::text, 2, '0')),
    Nombre VARCHAR(50) NOT NULL,
    Pais VARCHAR(50),
    Agente VARCHAR(10) REFERENCES Agente(Id_Agente),
    Id_Equipo VARCHAR(10) REFERENCES Equipo(Id_Equipo)
);

-- ==============================================================================
-- 3. TABLAS DE RELACIÓN Y ESTADÍSTICAS (Nivel 3)
-- ==============================================================================

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
    ID_Estadistica VARCHAR(10) PRIMARY KEY DEFAULT ('EP' || lpad(nextval('sec_est_partida')::text, 2, '0')),
    Puntuacion_equipo1 INTEGER,
    Puntuacion_equipo2 INTEGER,
    Duracion TIME,
    Id_PartidaFK VARCHAR(10) REFERENCES Partida(Id_Partida),
    Id_MapaFK VARCHAR(10) REFERENCES Mapa(Id_Mapa)
);

CREATE TABLE Estadistica_Jugador (
    Id_estadistica_jugador VARCHAR(10) PRIMARY KEY DEFAULT ('EJ' || lpad(nextval('sec_est_jugador')::text, 2, '0')),
    kills INTEGER DEFAULT 0,
    death INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    Id_PlayerFK VARCHAR(10) REFERENCES Jugador(Id_Player),
    Id_AgenteFK VARCHAR(10) REFERENCES Agente(Id_Agente),
    Id_Partido VARCHAR(10) REFERENCES Partida(Id_Partida)
);

CREATE TABLE Uso_Armas_Jugador (
    Id_Uso_Arma VARCHAR(10) PRIMARY KEY DEFAULT ('UA' || lpad(nextval('sec_uso_arma')::text, 2, '0')),
    Id_estadistica_jugadorFK VARCHAR(10) REFERENCES Estadistica_Jugador(Id_estadistica_jugador),
    Id_ArmaFK VARCHAR(10) REFERENCES Arma(Id_Arma),
    Kills_con_arma INTEGER DEFAULT 0,
    Dano_con_arma INTEGER DEFAULT 0
);

-- ==============================================================================
-- 4. TABLA DE AUDITORÍA (Mantenida intacta)
-- ==============================================================================
CREATE TABLE Audit_Log (
    Id_Audit SERIAL PRIMARY KEY,
    Tabla_Afectada VARCHAR(50),
    Operacion VARCHAR(20),
    Usuario VARCHAR(50),
    Fecha_Hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Detalle TEXT
);

-- ==========================================
-- ASIGNACIÓN DE PERMISOS A TABLAS RECIÉN CREADAS
-- ==========================================

-- Permisos para usuario_consulta (Solo lectura de todas las tablas actuales)
GRANT SELECT ON ALL TABLES IN SCHEMA public TO usuario_consulta;

-- Permisos para usuario_editor (CRUD de todas las tablas y uso de secuencias)
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO usuario_editor;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO usuario_editor;