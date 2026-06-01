-- ==========================================
-- 02-procedures.sql
-- Procedimientos y funciones almacenadas
-- ==========================================

-- ==========================================
-- FUNCIONES CRUD - JUGADOR
-- ==========================================

CREATE OR REPLACE FUNCTION sp_insertar_jugador(
    p_nombre VARCHAR,
    p_pais VARCHAR DEFAULT NULL,
    p_agente VARCHAR DEFAULT NULL,
    p_id_equipo VARCHAR DEFAULT NULL
)
RETURNS TABLE(id_player VARCHAR, nombre VARCHAR, pais VARCHAR, agente VARCHAR, id_equipo VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    INSERT INTO Jugador (Nombre, Pais, Agente, Id_Equipo)
    VALUES (p_nombre, p_pais, p_agente, p_id_equipo)
    RETURNING Jugador.Id_Player, Jugador.Nombre, Jugador.Pais, Jugador.Agente, Jugador.Id_Equipo;
END;
$$;

CREATE OR REPLACE FUNCTION sp_actualizar_jugador(
    p_id_player VARCHAR,
    p_nombre VARCHAR DEFAULT NULL,
    p_pais VARCHAR DEFAULT NULL,
    p_agente VARCHAR DEFAULT NULL,
    p_id_equipo VARCHAR DEFAULT NULL
)
RETURNS TABLE(id_player VARCHAR, nombre VARCHAR, pais VARCHAR, agente VARCHAR, id_equipo VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    UPDATE Jugador
    SET Nombre = COALESCE(p_nombre, Nombre),
        Pais = COALESCE(p_pais, Pais),
        Agente = COALESCE(p_agente, Agente),
        Id_Equipo = COALESCE(p_id_equipo, Id_Equipo),
        ultima_modificacion = CURRENT_TIMESTAMP
    WHERE Id_Player = p_id_player
    RETURNING Jugador.Id_Player, Jugador.Nombre, Jugador.Pais, Jugador.Agente, Jugador.Id_Equipo;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_eliminar_jugador(
    p_id_player VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM Estadistica_Jugador WHERE Id_PlayerFK = p_id_player;
    DELETE FROM Jugador WHERE Id_Player = p_id_player;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Jugador % no encontrado', p_id_player;
    END IF;
END;
$$;

-- ==========================================
-- FUNCIONES CRUD - EQUIPO
-- ==========================================

CREATE OR REPLACE FUNCTION sp_insertar_equipo(
    p_nombre_equipo VARCHAR,
    p_coach VARCHAR DEFAULT NULL,
    p_region VARCHAR DEFAULT NULL
)
RETURNS TABLE(id_equipo VARCHAR, nombre_equipo VARCHAR, coach VARCHAR, region VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    INSERT INTO Equipo (Nombre_Equipo, Coach, Region)
    VALUES (p_nombre_equipo, p_coach, p_region)
    RETURNING Equipo.Id_Equipo, Equipo.Nombre_Equipo, Equipo.Coach, Equipo.Region;
END;
$$;

CREATE OR REPLACE FUNCTION sp_actualizar_equipo(
    p_id_equipo VARCHAR,
    p_nombre_equipo VARCHAR DEFAULT NULL,
    p_coach VARCHAR DEFAULT NULL,
    p_region VARCHAR DEFAULT NULL
)
RETURNS TABLE(id_equipo VARCHAR, nombre_equipo VARCHAR, coach VARCHAR, region VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    UPDATE Equipo
    SET Nombre_Equipo = COALESCE(p_nombre_equipo, Nombre_Equipo),
        Coach = COALESCE(p_coach, Coach),
        Region = COALESCE(p_region, Region),
        ultima_modificacion = CURRENT_TIMESTAMP
    WHERE Id_Equipo = p_id_equipo
    RETURNING Equipo.Id_Equipo, Equipo.Nombre_Equipo, Equipo.Coach, Equipo.Region;
END;
$$;

-- ==========================================
-- FUNCIONES CRUD - PARTIDA
-- ==========================================

CREATE OR REPLACE FUNCTION sp_insertar_partida(
    p_id_partida VARCHAR,
    p_fecha DATE,
    p_fase INTEGER,
    p_id_torneofk VARCHAR,
    p_id_equipo1 VARCHAR,
    p_id_equipo2 VARCHAR,
    p_id_equipo_ganador VARCHAR
)
RETURNS TABLE(id_partida VARCHAR, fecha DATE, fase INTEGER, id_torneofk VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Partida (Id_Partida, fecha, Fase, Id_TorneoFK)
    VALUES (p_id_partida, p_fecha, p_fase, p_id_torneofk);

    INSERT INTO Partido_Equipo (Id_PartidaFK, Id_EquipoFK, Indicador_victoria)
    VALUES (p_id_partida, p_id_equipo1, p_id_equipo1 = p_id_equipo_ganador);

    INSERT INTO Partido_Equipo (Id_PartidaFK, Id_EquipoFK, Indicador_victoria)
    VALUES (p_id_partida, p_id_equipo2, p_id_equipo2 = p_id_equipo_ganador);

    RETURN QUERY
    SELECT p.Id_Partida, p.fecha, p.Fase, p.Id_TorneoFK
    FROM Partida p
    WHERE p.Id_Partida = p_id_partida;
END;
$$;

CREATE OR REPLACE FUNCTION sp_actualizar_partida(
    p_id_partida VARCHAR,
    p_fecha DATE DEFAULT NULL,
    p_fase INTEGER DEFAULT NULL,
    p_id_torneofk VARCHAR DEFAULT NULL
)
RETURNS TABLE(id_partida VARCHAR, fecha DATE, fase INTEGER, id_torneofk VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    UPDATE Partida
    SET fecha = COALESCE(p_fecha, fecha),
        Fase = COALESCE(p_fase, Fase),
        Id_TorneoFK = COALESCE(p_id_torneofk, Id_TorneoFK),
        ultima_modificacion = CURRENT_TIMESTAMP
    WHERE Id_Partida = p_id_partida
    RETURNING Partida.Id_Partida, Partida.fecha, Partida.Fase, Partida.Id_TorneoFK;
END;
$$;

-- ==========================================
-- FUNCIÓN - TORNEOS
-- ==========================================

CREATE OR REPLACE FUNCTION sp_obtener_torneos()
RETURNS TABLE(id_torneo VARCHAR, nombre VARCHAR, anio INTEGER, region VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT t.Id_Torneo, t.nombre_torneo,
           EXTRACT(YEAR FROM t.Fecha_inicio)::INTEGER AS anio,
           COALESCE(t.Region, 'Global') AS region
    FROM Torneo t
    ORDER BY t.Fecha_inicio DESC;
END;
$$;

-- ==========================================
-- FUNCIÓN CRUD - ESTADÍSTICA JUGADOR
-- ==========================================

CREATE OR REPLACE PROCEDURE sp_insertar_estadistica_jugador(
    p_id_est VARCHAR,
    p_kills INTEGER,
    p_death INTEGER,
    p_assists INTEGER,
    p_id_player VARCHAR,
    p_id_agente VARCHAR,
    p_id_partido VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Estadistica_Jugador (Id_estadistica_jugador, kills, death, assists, Id_PlayerFK, Id_AgenteFK, Id_Partido)
    VALUES (p_id_est, p_kills, p_death, p_assists, p_id_player, p_id_agente, p_id_partido);
END;
$$;

-- ==========================================
-- FUNCIONES DE CONSULTA ANALYTICS
-- ==========================================

CREATE OR REPLACE FUNCTION sp_obtener_leaderboard()
RETURNS TABLE(id_player VARCHAR, jugador VARCHAR, equipo VARCHAR, total_kills BIGINT, total_deaths BIGINT, kdr NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT v.id_player, v.jugador, v.equipo, v.total_kills, v.total_deaths, v.kdr
    FROM vista_kda_global v
    ORDER BY v.kdr DESC;
END;
$$;

CREATE OR REPLACE FUNCTION sp_obtener_map_stats_equipo(p_id_equipo VARCHAR)
RETURNS TABLE(mapa VARCHAR, jugadas BIGINT, victorias BIGINT, winrate NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT m.Nombre_Mapa::VARCHAR,
           COUNT(pe.id_partidafk)::BIGINT AS jugadas,
           COUNT(CASE WHEN pe.Indicador_victoria = TRUE THEN 1 END)::BIGINT AS victorias,
           ROUND((COUNT(CASE WHEN pe.Indicador_victoria = TRUE THEN 1 END)::NUMERIC / NULLIF(COUNT(pe.id_partidafk), 0)) * 100, 1) AS winrate
    FROM Partido_Equipo pe
    JOIN Estadistica_Partida ep ON pe.Id_PartidaFK = ep.Id_PartidaFK
    JOIN Mapa m ON ep.Id_MapaFK = m.Id_Mapa
    WHERE pe.Id_EquipoFK = p_id_equipo
    GROUP BY m.Nombre_Mapa
    ORDER BY winrate DESC;
END;
$$;

CREATE OR REPLACE FUNCTION sp_obtener_armas_jugador(p_id_player VARCHAR)
RETURNS TABLE(weapon VARCHAR, tipo VARCHAR, kills BIGINT, damage BIGINT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT a.Nombre_Arma::VARCHAR AS weapon,
           a.Tipo_de_arma::VARCHAR AS tipo,
           COALESCE(SUM(ua.Kills_con_arma), 0)::BIGINT AS kills,
           COALESCE(SUM(ua.Dano_con_arma), 0)::BIGINT AS damage
    FROM Uso_Armas_Jugador ua
    JOIN Arma a ON ua.Id_ArmaFK = a.Id_Arma
    JOIN Estadistica_Jugador ej ON ua.Id_estadistica_jugadorFK = ej.Id_estadistica_jugador
    WHERE ej.Id_PlayerFK = p_id_player
    GROUP BY a.Nombre_Arma, a.Tipo_de_arma
    ORDER BY kills DESC;
END;
$$;

CREATE OR REPLACE FUNCTION sp_obtener_meta_agentes()
RETURNS TABLE(agent VARCHAR, role VARCHAR, pickRate NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT v.nombre_agente::VARCHAR, r.nombre_rol::VARCHAR as role, v.pick_rate
    FROM vista_meta_agentes v
    JOIN rol r ON v.rol = r.cod_rol
    ORDER BY v.pick_rate DESC;
END;
$$;

CREATE OR REPLACE FUNCTION sp_obtener_recuento_partidas(
    p_torneo VARCHAR DEFAULT NULL,
    p_fase INTEGER DEFAULT NULL
)
RETURNS TABLE(
    id_partida VARCHAR, torneo VARCHAR, fase INTEGER, mapa VARCHAR,
    equipo_1 VARCHAR, equipo_2 VARCHAR, ganador VARCHAR,
    score_equipo_1 INTEGER, score_equipo_2 INTEGER,
    duracion VARCHAR, fecha VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT v.id_partida, v.torneo, v.fase, v.mapa,
           v.equipo_1, v.equipo_2, v.ganador,
           v.score_e1, v.score_e2,
           v.duracion::VARCHAR, v.fecha::VARCHAR
    FROM vista_detalles_partida v
    WHERE (p_torneo IS NULL OR v.torneo ILIKE '%' || p_torneo || '%')
      AND (p_fase IS NULL OR v.fase = p_fase)
    ORDER BY v.fecha DESC;
END;
$$;

-- ==========================================
-- FUNCIONES DE AUTENTICACIÓN
-- ==========================================

CREATE OR REPLACE PROCEDURE sp_registrar_usuario(
    p_username VARCHAR,
    p_password VARCHAR,
    p_rol VARCHAR DEFAULT 'Auditor'
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Usuario (username, password_hash, rol_usuario)
    VALUES (p_username, crypt(p_password, gen_salt('bf')), p_rol);
EXCEPTION
    WHEN unique_violation THEN
        RAISE EXCEPTION 'El nombre de usuario % ya existe', p_username;
END;
$$;

CREATE OR REPLACE FUNCTION sp_autenticar_usuario(
    p_username VARCHAR,
    p_password VARCHAR
)
RETURNS TABLE(username VARCHAR, rol_usuario VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT u.username, u.rol_usuario
    FROM Usuario u
    WHERE u.username = p_username
      AND u.password_hash = crypt(p_password, u.password_hash);
END;
$$;

-- ==========================================
-- PROCEDIMIENTO ORIGINAL (Registrar Partida Completa)
-- ==========================================

CREATE OR REPLACE PROCEDURE sp_registrar_partida(
    p_id_partida VARCHAR,
    p_fase INTEGER,
    p_id_torneo VARCHAR,
    p_id_mapa VARCHAR,
    p_id_equipo1 VARCHAR,
    p_id_equipo2 VARCHAR,
    p_score1 INTEGER,
    p_score2 INTEGER,
    p_duracion TIME
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Partida (Id_Partida, Fase, Id_TorneoFK, fecha)
    VALUES (p_id_partida, p_fase, p_id_torneo, CURRENT_DATE);

    INSERT INTO Partido_Equipo (Id_PartidaFK, Id_EquipoFK, Indicador_victoria)
    VALUES (p_id_partida, p_id_equipo1, p_score1 > p_score2);

    INSERT INTO Partido_Equipo (Id_PartidaFK, Id_EquipoFK, Indicador_victoria)
    VALUES (p_id_partida, p_id_equipo2, p_score2 > p_score1);

    INSERT INTO Estadistica_Partida (ID_Estadistica, Puntuacion_equipo1, Puntuacion_equipo2, Duracion, Id_PartidaFK, Id_MapaFK)
    VALUES ('EST' || p_id_partida, p_score1, p_score2, p_duracion, p_id_partida, p_id_mapa);

    RAISE NOTICE 'Partida % registrada exitosamente.', p_id_partida;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al registrar la partida: %', SQLERRM;
END;
$$;

-- ==========================================
-- PROCEDIMIENTO ORIGINAL (Actualizar KDA)
-- ==========================================

CREATE OR REPLACE PROCEDURE sp_actualizar_kda_jugador(
    p_id_est_jugador VARCHAR,
    p_kills INTEGER,
    p_deaths INTEGER,
    p_assists INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Estadistica_Jugador
    SET kills = p_kills,
        death = p_deaths,
        assists = p_assists
    WHERE Id_estadistica_jugador = p_id_est_jugador;
END;
$$;
