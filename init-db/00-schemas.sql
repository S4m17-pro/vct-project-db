-- ==========================================
-- 00-schemas.sql
-- Esquema completo de la base de datos VCT Stats
-- ==========================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Creación de Roles/Usuarios
DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'usuario_consulta') THEN CREATE USER usuario_consulta WITH PASSWORD 'consulta123'; END IF; END $$;
DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'usuario_editor') THEN CREATE USER usuario_editor WITH PASSWORD 'editor123'; END IF; END $$;

-- Privilegios básicos
GRANT CONNECT ON DATABASE vct_stats TO usuario_consulta;
GRANT USAGE ON SCHEMA public TO usuario_consulta;

GRANT CONNECT ON DATABASE vct_stats TO usuario_editor;
GRANT USAGE ON SCHEMA public TO usuario_editor;

-- Usuario Lewis
DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'lewis') THEN CREATE USER lewis WITH PASSWORD 'lewis123'; END IF; END $$;
GRANT CONNECT ON DATABASE vct_stats TO lewis;
GRANT USAGE ON SCHEMA public TO lewis;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO lewis;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO lewis;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO lewis;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO lewis;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO lewis;

CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol_usuario VARCHAR(20) DEFAULT 'Auditor' CHECK (rol_usuario IN ('Admin', 'Auditor'))
);

INSERT INTO Usuario (username, password_hash, rol_usuario) VALUES
('usuario_editor', crypt('editor123', gen_salt('bf')), 'Admin'),
('lewis', crypt('lewis123', gen_salt('bf')), 'Admin'),
('usuario_consulta', crypt('consulta123', gen_salt('bf')), 'Auditor')
ON CONFLICT (username) DO NOTHING;

-- ==========================================
-- 0. CREACIÓN DE SECUENCIAS
-- ==========================================
CREATE SEQUENCE IF NOT EXISTS sec_rol START WITH 5;
CREATE SEQUENCE IF NOT EXISTS sec_ultimate START WITH 29;
CREATE SEQUENCE IF NOT EXISTS sec_mapa START WITH 12;
CREATE SEQUENCE IF NOT EXISTS sec_equipo START WITH 13;
CREATE SEQUENCE IF NOT EXISTS sec_torneo START WITH 2;
CREATE SEQUENCE IF NOT EXISTS sec_arma START WITH 4;
CREATE SEQUENCE IF NOT EXISTS sec_agente START WITH 29;
CREATE SEQUENCE IF NOT EXISTS sec_habilidad START WITH 29;
CREATE SEQUENCE IF NOT EXISTS sec_partida START WITH 4;
CREATE SEQUENCE IF NOT EXISTS sec_jugador START WITH 11;
CREATE SEQUENCE IF NOT EXISTS sec_est_partida START WITH 4;
CREATE SEQUENCE IF NOT EXISTS sec_est_jugador START WITH 9;
CREATE SEQUENCE IF NOT EXISTS sec_uso_arma START WITH 3;

-- ==========================================
-- 1. TABLAS INDEPENDIENTES (Nivel 1)
-- ==========================================
CREATE TABLE IF NOT EXISTS Rol (
    Cod_Rol VARCHAR(10) PRIMARY KEY DEFAULT ('R' || lpad(nextval('sec_rol')::text, 2, '0')),
    Nombre_Rol VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Ultimate (
    Id_Ultimate VARCHAR(10) PRIMARY KEY DEFAULT ('U' || lpad(nextval('sec_ultimate')::text, 2, '0')),
    Nombre_Ultimate VARCHAR(60) NOT NULL,
    Dano INTEGER,
    Puntos_de_ulti INTEGER,
    Tiempo_de_activacion FLOAT
);

CREATE TABLE IF NOT EXISTS Mapa (
    Id_Mapa VARCHAR(10) PRIMARY KEY DEFAULT ('M' || lpad(nextval('sec_mapa')::text, 2, '0')),
    Nombre_Mapa VARCHAR(30) NOT NULL,
    Ubicacion VARCHAR(50),
    Cantidad_Orbes INTEGER,
    Cantidad_Sites INTEGER
);

CREATE TABLE IF NOT EXISTS Equipo (
    Id_Equipo VARCHAR(10) PRIMARY KEY DEFAULT ('E' || lpad(nextval('sec_equipo')::text, 2, '0')),
    Nombre_Equipo VARCHAR(50) NOT NULL,
    Coach VARCHAR(50),
    Region VARCHAR(50),
    ultima_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Torneo (
    Id_Torneo VARCHAR(10) PRIMARY KEY DEFAULT ('T' || lpad(nextval('sec_torneo')::text, 2, '0')),
    nombre_torneo VARCHAR(50) NOT NULL,
    Region VARCHAR(50),
    Fecha_inicio DATE,
    Fecha_fin DATE,
    Ubicacion VARCHAR(50),
    Premio_total BIGINT,
    ultima_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Arma (
    Id_Arma VARCHAR(10) PRIMARY KEY DEFAULT ('A' || lpad(nextval('sec_arma')::text, 2, '0')),
    Nombre_Arma VARCHAR(30) NOT NULL,
    Creditos INTEGER,
    Tipo_de_arma VARCHAR(30),
    Tiempo_de_recarga FLOAT,
    Balas_de_Cargador INTEGER,
    Total_de_balas INTEGER,
    Modo_de_disparo VARCHAR(30)
);

-- ==========================================
-- 2. TABLAS CON DEPENDENCIAS (Nivel 2)
-- ==========================================
CREATE TABLE IF NOT EXISTS Agente (
    Id_Agente VARCHAR(10) PRIMARY KEY DEFAULT ('AG' || lpad(nextval('sec_agente')::text, 2, '0')),
    Nombre_Agente VARCHAR(30) NOT NULL,
    Rol VARCHAR(10) REFERENCES Rol(Cod_Rol)
);

CREATE TABLE IF NOT EXISTS Habilidad (
    Id_Habilidad VARCHAR(10) PRIMARY KEY DEFAULT ('H' || lpad(nextval('sec_habilidad')::text, 2, '0')),
    Nombre_Habilidad VARCHAR(60) NOT NULL,
    Tecla VARCHAR(1),
    Dano INTEGER,
    Cargas INTEGER,
    Tiempo_de_activacion FLOAT,
    Id_UltimateFK VARCHAR(10) REFERENCES Ultimate(Id_Ultimate)
);

CREATE TABLE IF NOT EXISTS Partida (
    Id_Partida VARCHAR(10) PRIMARY KEY DEFAULT ('P' || lpad(nextval('sec_partida')::text, 2, '0')),
    fecha DATE DEFAULT CURRENT_DATE,
    Fase INTEGER,
    Id_TorneoFK VARCHAR(10) REFERENCES Torneo(Id_Torneo),
    ultima_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Jugador (
    Id_Player VARCHAR(10) PRIMARY KEY DEFAULT ('J' || lpad(nextval('sec_jugador')::text, 2, '0')),
    Nombre VARCHAR(50) NOT NULL,
    Pais VARCHAR(50),
    Agente VARCHAR(10) REFERENCES Agente(Id_Agente),
    Id_Equipo VARCHAR(10) REFERENCES Equipo(Id_Equipo),
    ultima_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- 3. TABLAS DE RELACIÓN Y ESTADÍSTICAS (Nivel 3)
-- ==========================================
CREATE TABLE IF NOT EXISTS Agente_Habilidad (
    Id_AgenteFK VARCHAR(10) REFERENCES Agente(Id_Agente),
    Id_HabilidadFK VARCHAR(10) REFERENCES Habilidad(Id_Habilidad),
    Orden_Habilidad INTEGER,
    PRIMARY KEY (Id_AgenteFK, Id_HabilidadFK)
);

CREATE TABLE IF NOT EXISTS Partido_Equipo (
    Id_PartidaFK VARCHAR(10) REFERENCES Partida(Id_Partida),
    Id_EquipoFK VARCHAR(10) REFERENCES Equipo(Id_Equipo),
    Indicador_victoria BOOLEAN,
    PRIMARY KEY (Id_PartidaFK, Id_EquipoFK)
);

CREATE TABLE IF NOT EXISTS Estadistica_Partida (
    ID_Estadistica VARCHAR(10) PRIMARY KEY DEFAULT ('EP' || lpad(nextval('sec_est_partida')::text, 2, '0')),
    Puntuacion_equipo1 INTEGER,
    Puntuacion_equipo2 INTEGER,
    Duracion TIME,
    Id_PartidaFK VARCHAR(10) REFERENCES Partida(Id_Partida),
    Id_MapaFK VARCHAR(10) REFERENCES Mapa(Id_Mapa)
);

CREATE TABLE IF NOT EXISTS Estadistica_Jugador (
    Id_estadistica_jugador VARCHAR(10) PRIMARY KEY DEFAULT ('EJ' || lpad(nextval('sec_est_jugador')::text, 2, '0')),
    kills INTEGER DEFAULT 0,
    death INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    Id_PlayerFK VARCHAR(10) REFERENCES Jugador(Id_Player),
    Id_AgenteFK VARCHAR(10) REFERENCES Agente(Id_Agente),
    Id_Partido VARCHAR(10) REFERENCES Partida(Id_Partida)
);

CREATE TABLE IF NOT EXISTS Uso_Armas_Jugador (
    Id_Uso_Arma VARCHAR(10) PRIMARY KEY DEFAULT ('UA' || lpad(nextval('sec_uso_arma')::text, 2, '0')),
    Id_estadistica_jugadorFK VARCHAR(10) REFERENCES Estadistica_Jugador(Id_estadistica_jugador),
    Id_ArmaFK VARCHAR(10) REFERENCES Arma(Id_Arma),
    Kills_con_arma INTEGER DEFAULT 0,
    Dano_con_arma INTEGER DEFAULT 0
);

-- ==========================================
-- 4. TABLA DE AUDITORÍA
-- ==========================================
CREATE TABLE IF NOT EXISTS Audit_Log (
    Id_Audit SERIAL PRIMARY KEY,
    Tabla_Afectada VARCHAR(50),
    Operacion VARCHAR(20),
    Usuario VARCHAR(50),
    Fecha_Hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Detalle TEXT
);

-- ==========================================
-- ASIGNACIÓN DE PERMISOS
-- ==========================================
GRANT SELECT ON ALL TABLES IN SCHEMA public TO usuario_consulta;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO usuario_editor;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO usuario_editor;
