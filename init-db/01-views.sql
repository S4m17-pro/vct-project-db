-- ==========================================
-- 01-views.sql
-- Vistas para el análisis de estadísticas de VCT
-- ==========================================

-- 1. Vista Resumen de Jugadores (Ranking)
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
CREATE OR REPLACE VIEW vista_detalles_partida AS
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
    t.nombre_torneo AS torneo,
    m.nombre_mapa AS mapa,
    p.fase,
    p.fecha,
    ep.puntuacion_equipo1 AS score_e1,
    ep.puntuacion_equipo2 AS score_e2,
    ep.duracion,
    e1.nombre_equipo AS equipo_1,
    e2.nombre_equipo AS equipo_2,
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

-- 4. Vista Meta Agentes (Pick Rate)
DROP VIEW IF EXISTS vista_meta_agentes CASCADE;
CREATE OR REPLACE VIEW vista_meta_agentes AS
WITH total_partidas AS (
    SELECT COUNT(DISTINCT id_partida) AS total FROM partida
),
conteos AS (
    SELECT
        id_agentefk,
        COUNT(*) AS veces_elegido
    FROM estadistica_jugador
    GROUP BY id_agentefk
)
SELECT
    a.nombre_agente,
    a.rol,
    c.veces_elegido,
    ROUND((c.veces_elegido::numeric / (SELECT total FROM total_partidas)) * 100, 1) AS pick_rate
FROM conteos c
JOIN agente a ON c.id_agentefk = a.id_agente
ORDER BY pick_rate DESC;

-- 5. Vista KDA Global (Leaderboard)
CREATE OR REPLACE VIEW vista_kda_global AS
SELECT
    j.id_player,
    j.Nombre AS jugador,
    e.Nombre_Equipo AS equipo,
    COALESCE(SUM(ej.kills), 0) AS total_kills,
    COALESCE(SUM(ej.death), 0) AS total_deaths,
    COALESCE(SUM(ej.assists), 0) AS total_assists,
    ROUND(SUM(ej.kills)::numeric / NULLIF(SUM(ej.death), 0), 2) AS kdr
FROM Jugador j
LEFT JOIN Equipo e ON j.Id_Equipo = e.Id_Equipo
LEFT JOIN Estadistica_Jugador ej ON j.Id_Player = ej.Id_PlayerFK
GROUP BY j.id_player, j.Nombre, e.Nombre_Equipo
ORDER BY kdr DESC;

-- 6. Vista Armas Populares
CREATE OR REPLACE VIEW vista_armas_populares AS
SELECT
    a.Nombre_Arma AS arma,
    a.Tipo_de_arma AS tipo_arma,
    COALESCE(SUM(ua.Kills_con_arma), 0) AS total_kills,
    COALESCE(SUM(ua.Dano_con_arma), 0) AS total_dano
FROM Arma a
LEFT JOIN Uso_Armas_Jugador ua ON a.Id_Arma = ua.Id_ArmaFK
GROUP BY a.Nombre_Arma, a.Tipo_de_arma
ORDER BY total_kills DESC;

-- 7. Vista Rendimiento Agentes por Mapa
CREATE OR REPLACE VIEW vista_rendimiento_agentes_mapa AS
SELECT
    a.Nombre_Agente AS agente,
    r.Nombre_Rol AS rol_agente,
    m.Nombre_Mapa AS mapa,
    COUNT(DISTINCT ej.Id_estadistica_jugador) AS veces_jugado,
    ROUND(AVG(ej.kills), 1) AS avg_kills,
    ROUND(AVG(ej.death), 1) AS avg_deaths,
    ROUND(AVG(ej.assists), 1) AS avg_assists,
    ROUND((AVG(ej.kills + ej.assists))::numeric / NULLIF(AVG(ej.death), 0), 2) AS avg_kda
FROM Estadistica_Jugador ej
JOIN Agente a ON ej.Id_AgenteFK = a.Id_Agente
JOIN Rol r ON a.Rol = r.Cod_Rol
JOIN Partida p ON ej.Id_Partido = p.Id_Partida
JOIN Estadistica_Partida ep ON p.Id_Partida = ep.Id_PartidaFK
JOIN Mapa m ON ep.Id_MapaFK = m.Id_Mapa
GROUP BY a.Nombre_Agente, r.Nombre_Rol, m.Nombre_Mapa
ORDER BY avg_kda DESC;

-- 8. Vista Historial de Jugador
CREATE OR REPLACE VIEW vista_historial_jugador AS
SELECT
    j.Id_Player AS id_player,
    j.Nombre AS jugador,
    p.Id_Partida AS id_partida,
    p.fecha,
    t.nombre_torneo AS torneo,
    m.Nombre_Mapa AS mapa,
    a.Nombre_Agente AS agente_usado,
    ej.kills,
    ej.death,
    ej.assists,
    ROUND((ej.kills + ej.assists)::numeric / NULLIF(ej.death, 0), 2) AS kda_partida
FROM Jugador j
JOIN Estadistica_Jugador ej ON j.Id_Player = ej.Id_PlayerFK
JOIN Partida p ON ej.Id_Partido = p.Id_Partida
JOIN Torneo t ON p.Id_TorneoFK = t.Id_Torneo
JOIN Estadistica_Partida ep ON p.Id_Partida = ep.Id_PartidaFK
JOIN Mapa m ON ep.Id_MapaFK = m.Id_Mapa
JOIN Agente a ON ej.Id_AgenteFK = a.Id_Agente
ORDER BY p.fecha DESC;

-- 9. Vista Estadísticas de Torneo
CREATE OR REPLACE VIEW vista_estadisticas_torneo AS
SELECT
    t.Id_Torneo AS id_torneo,
    t.nombre_torneo AS torneo,
    t.Region AS region,
    p.Id_Partida AS id_partida,
    p.fase,
    m.Nombre_Mapa AS mapa,
    ep.Puntuacion_equipo1 AS score_equipo_1,
    ep.Puntuacion_equipo2 AS score_equipo_2,
    (SELECT e1.Nombre_Equipo FROM Partido_Equipo pe1
     JOIN Equipo e1 ON pe1.Id_EquipoFK = e1.Id_Equipo
     WHERE pe1.Id_PartidaFK = p.Id_Partida ORDER BY pe1.Id_EquipoFK LIMIT 1) AS equipo_1,
    (SELECT e2.Nombre_Equipo FROM Partido_Equipo pe2
     JOIN Equipo e2 ON pe2.Id_EquipoFK = e2.Id_Equipo
     WHERE pe2.Id_PartidaFK = p.Id_Partida ORDER BY pe2.Id_EquipoFK DESC LIMIT 1) AS equipo_2,
    (SELECT e3.Nombre_Equipo FROM Partido_Equipo pe3
     JOIN Equipo e3 ON pe3.Id_EquipoFK = e3.Id_Equipo
     WHERE pe3.Id_PartidaFK = p.Id_Partida AND pe3.Indicador_victoria = TRUE LIMIT 1) AS ganador
FROM Torneo t
JOIN Partida p ON t.Id_Torneo = p.Id_TorneoFK
JOIN Estadistica_Partida ep ON p.Id_Partida = ep.Id_PartidaFK
JOIN Mapa m ON ep.Id_MapaFK = m.Id_Mapa
ORDER BY t.nombre_torneo, p.fecha;

-- Permisos para las vistas
GRANT SELECT ON Vista_Resumen_Jugadores, Vista_Estadisticas_Equipos, Vista_Detalles_Partida TO usuario_consulta, usuario_editor, lewis;
