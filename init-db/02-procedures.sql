-- ==========================================
-- 02-procedures.sql
-- Descripción: Procedimientos almacenados para manipulación de datos
-- ==========================================

-- 1. Procedimiento para Registrar una Partida Completa
-- Inserta en Partida y Estadistica_Partida en una sola operación
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
    -- Insertar en la tabla de Partida
    INSERT INTO Partida (Id_Partida, Fase, Id_TorneoFK, fecha)
    VALUES (p_id_partida, p_fase, p_id_torneo, CURRENT_DATE);

    -- Insertar la relacion de los equipos con la partida y quien ganó
    INSERT INTO Partido_Equipo (Id_PartidaFK, Id_EquipoFK, Indicador_victoria)
    VALUES (p_id_partida, p_id_equipo1, p_score1 > p_score2);

    INSERT INTO Partido_Equipo (Id_PartidaFK, Id_EquipoFK, Indicador_victoria)
    VALUES (p_id_partida, p_id_equipo2, p_score2 > p_score1);

    -- Insertar en las estadísticas de la partida
    INSERT INTO Estadistica_Partida (ID_Estadistica, Puntuacion_equipo1, Puntuacion_equipo2, Duracion, Id_PartidaFK, Id_MapaFK)
    VALUES ('EST' || p_id_partida, p_score1, p_score2, p_duracion, p_id_partida, p_id_mapa);

    COMMIT;
    RAISE NOTICE 'Partida % registrada exitosamente con sus estadísticas.', p_id_partida;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE EXCEPTION 'Error al registrar la partida: %', SQLERRM;
END;
$$;

-- 2. Procedimiento para Actualizar KDA de Jugador
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

    COMMIT;
END;
$$;
