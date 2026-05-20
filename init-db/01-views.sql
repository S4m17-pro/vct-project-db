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
CREATE OR REPLACE VIEW Vista_Detalles_Partida AS
SELECT 
    p.Id_Partida,
    t.nombre_torneo AS Torneo,
    m.Nombre_Mapa AS Mapa,
    ep.Puntuacion_equipo1 AS Score_E1,
    ep.Puntuacion_equipo2 AS Score_E2,
    ep.Duracion,
    p.fecha
FROM Partida p
JOIN Torneo t ON p.Id_TorneoFK = t.Id_Torneo
JOIN Estadistica_Partida ep ON p.Id_Partida = ep.Id_PartidaFK
JOIN Mapa m ON ep.Id_MapaFK = m.Id_Mapa;

-- OTORGAR PERMISOS A LAS VISTAS
-- Esto arregla el error de "permission denied" porque las vistas se crean después del GRANT inicial
GRANT SELECT ON Vista_Resumen_Jugadores, Vista_Estadisticas_Equipos, Vista_Detalles_Partida TO usuario_consulta, usuario_editor, lewis;
