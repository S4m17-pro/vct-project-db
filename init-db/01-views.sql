-- ==========================================
-- 01-views.sql
-- Descripción: Vistas para el análisis de estadísticas de VCT
-- ==========================================

-- 1. Vista Resumen de Jugadores (Ranking)
-- Une Jugador, Equipo y Estadísticas para mostrar el KDA
CREATE OR REPLACE VIEW Vista_Resumen_Jugadores AS
SELECT 
    j.Nombre AS Jugador,
    e.Nombre_Equipo AS Equipo,
    a.Nombre_Agente AS Agente,
    ej.kills,
    ej.death,
    ej.assists,
    ROUND((ej.kills + ej.assists)::NUMERIC / GREATEST(ej.death, 1), 2) AS KDA
FROM Jugador j
JOIN Equipo e ON j.Id_Equipo = e.Id_Equipo
JOIN Agente a ON j.Agente = a.Id_Agente
JOIN Estadistica_Jugador ej ON j.Id_Player = ej.Id_PlayerFK;

-- 2. Vista Desempeño de Equipos
-- Muestra el total de victorias por equipo
CREATE OR REPLACE VIEW Vista_Estadisticas_Equipos AS
SELECT 
    e.Nombre_Equipo,
    COUNT(pe.Id_PartidaFK) AS Partidas_Jugadas,
    COUNT(CASE WHEN pe.Indicador_victoria = TRUE THEN 1 END) AS Victorias,
    COUNT(CASE WHEN pe.Indicador_victoria = FALSE THEN 1 END) AS Derrotas
FROM Equipo e
LEFT JOIN Partido_Equipo pe ON e.Id_Equipo = pe.Id_EquipoFK
GROUP BY e.Nombre_Equipo;

-- 3. Vista Detalles de Partida
-- Une Partida, Torneo y Estadísticas de Mapa

CREATE VIEW vista_detalles_partida AS
WITH posiciones AS (
    SELECT 
        pe.id_partidafk,
        pe.id_equipofk,
        eq.nombre_equipo,
        pe.indicador_victoria,
        ROW_NUMBER() OVER (PARTITION BY pe.id_partidafk ORDER BY pe.id_equipofk) as rn
    FROM partido_equipo pe
    JOIN equipo eq ON pe.id_equipofk = eq.id_equipo
)
SELECT 
    p.id_partida,
    t.nombre_torneo AS torneo,            -- Mapeado con la columna exacta
    m.nombre_mapa AS mapa,                -- Mapeado con la columna exacta
    p.fase,
    p.fecha,
    ep.puntuacion_equipo1 AS score_e1, 
    ep.puntuacion_equipo2 AS score_e2,
    ep.duracion,
    -- Nombres comerciales de los equipos para las tarjetas y las tablas
    e1.nombre_equipo AS equipo_1,
    e2.nombre_equipo AS equipo_2,
    -- El residuo del ganador se calcula devolviendo el nombre del equipo que tenga 'true'
    CASE 
        WHEN e1.indicador_victoria = true THEN e1.nombre_equipo
        ELSE e2.nombre_equipo
    END AS ganador
FROM partida p
JOIN torneo t ON p.id_torneofk = t.id_torneo
JOIN estadistica_partida ep ON p.id_partida = ep.id_partidafk
JOIN mapa m ON ep.id_mapafk = m.id_mapa
LEFT JOIN posiciones e1 ON p.id_partida = e1.id_partidafk AND e1.rn = 1
LEFT JOIN posiciones e2 ON p.id_partida = e2.id_partidafk AND e2.rn = 2;

DROP VIEW IF EXISTS vista_meta_agentes CASCADE;

CREATE VIEW vista_meta_agentes AS
WITH total_partidas AS (
    SELECT COUNT(DISTINCT id_partida) AS total FROM partida
),
conteos AS (
    SELECT 
        id_agentefk, -- Ajusta si se llama id_agente o similar
        COUNT(*) AS veces_elegido
    FROM estadistica_jugador -- Tu tabla de estadísticas de jugador
    GROUP BY id_agentefk
)
SELECT 
    a.nombre_agente, -- O el campo de texto con el nombre (ej: Jett, Omen)
    a.rol,           -- Opcional: Duelista, Controlador, etc.
    c.veces_elegido,
    -- Porcentaje: (veces_elegido / total_partidas) * 100
    ROUND((c.veces_elegido::numeric / (SELECT total FROM total_partidas)) * 100, 1) AS pick_rate
FROM conteos c
JOIN agente a ON c.id_agentefk = a.id_agente -- Ajusta según tu maestro de agentes
ORDER BY pick_rate DESC;

-- OTORGAR PERMISOS A LAS VISTAS
-- Esto arregla el error de "permission denied" porque las vistas se crean después del GRANT inicial
GRANT SELECT ON Vista_Resumen_Jugadores, Vista_Estadisticas_Equipos, Vista_Detalles_Partida TO usuario_consulta, usuario_editor, lewis;
