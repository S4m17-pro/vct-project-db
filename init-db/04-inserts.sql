-- ==========================================
-- 04-inserts.sql
-- Descripción: Datos de prueba (Mock Data) para VCT Stats
-- ==========================================

-- ==========================================
-- NIVEL 1: Tablas Independientes
-- ==========================================

-- Roles
INSERT INTO Rol (Cod_Rol, Nombre_Rol) VALUES
('R01', 'Duelista'),
('R02', 'Controlador'),
('R03', 'Iniciador'),
('R04', 'Centinela');

-- Ultimates
INSERT INTO Ultimate (Id_Ultimate, Nombre_Ultimate, Dano, Puntos_de_ulti, Tiempo_de_activacion) VALUES
('U01', 'Tormenta de Cuchillas', 50, 7, 1.5),
('U02', 'Tumba Viper', 0, 8, 2.0),
('U03', 'Tumba de Bajas', 150, 8, 1.0);

-- Mapas
INSERT INTO Mapa (Id_Mapa, Nombre_Mapa, Ubicacion, Cantidad_Orbes, Cantidad_Sites) VALUES
('M01', 'Ascent', 'Italia', 2, 2),
('M02', 'Bind', 'Marruecos', 2, 2),
('M03', 'Lotus', 'India', 3, 3);

-- Equipos
INSERT INTO Equipo (Id_Equipo, Nombre_Equipo, Coach, Region) VALUES
('E01', 'KRU Esports', 'Atom', 'Americas'),
('E02', 'Leviatán', 'Goked', 'Americas'),
('E03', 'LOUD', 'Peu', 'Americas');

-- Torneos
INSERT INTO Torneo (Id_Torneo, nombre_torneo, Region, Fecha_inicio, Fecha_fin, Ubicacion, Premio_total) VALUES
('T01', 'VCT Americas Stage 1', 'Americas', '2026-04-01', '2026-05-15', 'Los Angeles', 500000);

-- Armas
INSERT INTO Arma (Id_Arma, Nombre_Arma, Creditos, Tipo_de_arma, Tiempo_de_recarga, Balas_de_Cargador, Total_de_balas, Modo_de_disparo) VALUES
('A01', 'Vandal', 2900, 'Rifle', 2.5, 25, 75, 'Automático'),
('A02', 'Phantom', 2900, 'Rifle', 2.5, 30, 90, 'Automático'),
('A03', 'Operator', 4700, 'Francotirador', 3.7, 5, 15, 'Semiautomático');

-- ==========================================
-- NIVEL 2: Tablas con Dependencias
-- ==========================================

-- Agentes
INSERT INTO Agente (Id_Agente, Nombre_Agente, Rol) VALUES
('AG01', 'Jett', 'R01'),
('AG02', 'Viper', 'R02'),
('AG03', 'Raze', 'R01'),
('AG04', 'Omen', 'R02');

-- Habilidades
INSERT INTO Habilidad (Id_Habilidad, Nombre_Habilidad, Tecla, Dano, Cargas, Tiempo_de_activacion, Id_UltimateFK) VALUES
('H01', 'Impulso', 'Q', 0, 2, 0.5, 'U01'),
('H02', 'Nube Venenosa', 'Q', 0, 1, 0.5, 'U02');

-- Partidas
INSERT INTO Partida (Id_Partida, fecha, Fase, Id_TorneoFK) VALUES
('P01', '2026-04-10', 1, 'T01'),
('P02', '2026-04-12', 1, 'T01');

-- Jugadores
INSERT INTO Jugador (Id_Player, Nombre, Pais, Agente, Id_Equipo) VALUES
('J01', 'Keznit', 'Chile', 'AG03', 'E01'),
('J02', 'Melser', 'Chile', 'AG04', 'E01'),
('J03', 'Aspas', 'Brasil', 'AG01', 'E02'),
('J04', 'Mazino', 'Chile', 'AG04', 'E02'),
('J05', 'Less', 'Brasil', 'AG02', 'E03');

-- ==========================================
-- NIVEL 3: Tablas Relacionales y Estadísticas
-- ==========================================

-- Agente_Habilidad
INSERT INTO Agente_Habilidad (Id_AgenteFK, Id_HabilidadFK, Orden_Habilidad) VALUES
('AG01', 'H01', 1),
('AG02', 'H02', 1);

-- Partido_Equipo (P01: KRU vs Leviatán, gana Leviatán)
INSERT INTO Partido_Equipo (Id_PartidaFK, Id_EquipoFK, Indicador_victoria) VALUES
('P01', 'E01', FALSE),
('P01', 'E02', TRUE);

-- Partido_Equipo (P02: LOUD vs KRU, gana LOUD)
INSERT INTO Partido_Equipo (Id_PartidaFK, Id_EquipoFK, Indicador_victoria) VALUES
('P02', 'E03', TRUE),
('P02', 'E01', FALSE);

-- Estadistica_Partida
INSERT INTO Estadistica_Partida (ID_Estadistica, Puntuacion_equipo1, Puntuacion_equipo2, Duracion, Id_PartidaFK, Id_MapaFK) VALUES
('EP01', 11, 13, '00:45:00', 'P01', 'M01'),
('EP02', 13, 9, '00:38:00', 'P02', 'M02');

-- Estadistica_Jugador (Kills, Deaths, Assists)
INSERT INTO Estadistica_Jugador (Id_estadistica_jugador, kills, death, assists, Id_PlayerFK, Id_AgenteFK, Id_Partido) VALUES
-- Partida 1: KRU vs LEV
('EJ01', 25, 18, 5, 'J01', 'AG03', 'P01'), -- Keznit
('EJ02', 28, 15, 4, 'J03', 'AG01', 'P01'), -- Aspas
('EJ03', 12, 16, 15, 'J04', 'AG04', 'P01'), -- Mazino

-- Partida 2: LOUD vs KRU
('EJ04', 22, 14, 8, 'J05', 'AG02', 'P02'), -- Less
('EJ05', 18, 19, 6, 'J01', 'AG03', 'P02'); -- Keznit

-- Uso_Armas_Jugador
INSERT INTO Uso_Armas_Jugador (Id_Uso_Arma, Id_estadistica_jugadorFK, Id_ArmaFK, Kills_con_arma, Dano_con_arma) VALUES
('UA01', 'EJ01', 'A01', 20, 3000), -- Keznit Vandal
('UA02', 'EJ02', 'A03', 15, 2250); -- Aspas Operator
