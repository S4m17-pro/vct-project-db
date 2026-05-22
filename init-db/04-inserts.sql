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
('U01', 'Tormenta de Cuchillas', 50, 7, 1.5), -- Jett (AG01)
('U02', 'Pozo de la Víbora', 0, 8, 2.0),       -- Viper (AG02)
('U03', 'Tumba de Bajas', 150, 8, 1.0),       -- Raze (AG03)
('U04', 'Desde las Sombras', 0, 7, 2.5),       -- Omen (AG04)
('U05', 'Pozo de Gravedad', 0, 8, 1.0),        -- Astra (AG05)
('U06', 'Trueno Retumbante', 0, 8, 2.2),       -- Breach (AG06)
('U07', 'Golpe Orbital', 150, 8, 3.0),         -- Brimstone (AG07)
('U08', 'Cazador de Cabezas', 100, 8, 0.5),    -- Chamber (AG08)
('U09', 'Aún No Muero', 0, 8, 2.0),            -- Clove (AG09)
('U10', 'Hurto de Neuronas', 0, 7, 1.0),       -- Cypher (AG10)
('U11', 'Aniquilación', 150, 8, 2.0),          -- Deadlock (AG11)
('U12', 'Ocaso', 0, 8, 2.0),                   -- Fade (AG12)
('U13', 'X_D_I_S_T_A_N_C_I_A', 0, 8, 1.5),     -- Gekko (AG13)
('U14', 'Bloqueo', 0, 9, 3.0),                 -- Killjoy (AG14)
('U15', 'Aullido de Ajuste', 0, 7, 1.5),       -- Harbor (AG15)
('U16', 'Matar por Contrato', 150, 7, 1.0),    -- Iso (AG16)
('U17', 'NULL/cmd', 0, 8, 1.0),                -- KAY/O (AG17)
('U18', 'Sobrecarga', 0, 7, 1.0),              -- Neon (AG18)
('U19', 'Fénix Renacido', 0, 8, 1.0),          -- Phoenix (AG19)
('U20', 'Empatía de la Emperatriz', 0, 7, 0.5),-- Reyna (AG20)
('U21', 'Resurrección', 0, 9, 2.5),            -- Sage (AG21)
('U22', 'Buscadores', 0, 7, 1.5),              -- Skye (AG22)
('U23', 'Furia del Cazador', 80, 8, 1.5),       -- Sova (AG23)
('U24', 'Golpe Sísmico Regional', 120, 8, 2.0),-- Tejo (AG24)
('U25', 'Línea de Bloqueo', 100, 7, 1.0),      -- Veto (AG25)
('U26', 'Jardín de Acero', 0, 8, 2.0),          -- Vyse (AG26)
('U27', 'Camino del Mañana', 120, 8, 1.8),     -- Waylay (AG27)
('U28', 'Cambio de Dimensión', 0, 7, 1.0);     -- Yoru (AG28)

-- Mapas
INSERT INTO Mapa (Id_Mapa, Nombre_Mapa, Ubicacion, Cantidad_Orbes, Cantidad_Sites) VALUES
('M01', 'Ascent', 'Italia', 2, 2),
('M02', 'Bind', 'Marruecos', 2, 2),
('M03', 'Lotus', 'India', 3, 3)
('M04', 'Haven', 'Bután', 2, 3),
('M05', 'Split', 'Japón', 2, 2),
('M06', 'Icebox', 'Rusia', 2, 2),
('M07', 'Breeze', 'Triángulo de las Bermudas', 2, 2),
('M08', 'Fracture', 'Estados Unidos', 4, 2),
('M09', 'Pearl', 'Portugal', 2, 2),
('M10', 'Sunset', 'Estados Unidos', 2, 2),
('M11', 'Abyss', 'Islandia', 2, 2);

-- Equipos
INSERT INTO Equipo (Nombre_Equipo, Coach, Region) VALUES
('KRU Esports', 'Atom', 'Americas'),
('Leviatán', 'Goked', 'Americas'),
('LOUD', 'Peu', 'Americas')
('Sentinels', 'kaplan', 'Americas'),
('100 Thieves', 'Zikz', 'Americas'),
('Cloud9', 'Immi', 'Americas'),
('Evil Geniuses', 'Potter', 'Americas'),
('NRG', 'Chet', 'Americas'),
('FURIA Esports', 'In切り', 'Americas'),
('MIBR', 'fRoD', 'Americas'),
('G2 Esports', 'JoshRT', 'Americas'),
('KRU Elite', 'Atom', 'Americas'),
-- Región: EMEA (Europa)
('Fnatic', 'Elmapuddy', 'EMEA'),
('Natus Vincere', 'd00mbros', 'EMEA'),
('Team Vitality', 'Salah', 'EMEA'),
('Team Heretics', 'Neilzinho', 'EMEA'), 
('Karmine Corp', 'Engh', 'EMEA'),
('FUT Esports', 'GAIS', 'EMEA'),

-- Región: Pacific (Asia-Pacífico)
('Paper Rex', 'alecks', 'Pacific'),
('DRX', 'Termi', 'Pacific'),
('Gen.G Esports', 'solo', 'Pacific'),
('T1', 'Autumn', 'Pacific'),
('ZETA DIVISION', 'Carlao', 'Pacific'),
('Team Secret', 'Warbirds', 'Pacific'),

-- Región: China
('EDward Gaming', 'Muggle', 'China'),
('FunPlus Phoenix', 'NaVi', 'China'),
('Trace Esports', 'Feng', 'China'),
('All Gamers', 'Yi', 'China');

-- Torneos
INSERT INTO Torneo (nombre_torneo, Region, Fecha_inicio, Fecha_fin, Ubicacion, Premio_total) VALUES
('VCT Americas Stage 1', 'Americas', '2026-04-01', '2026-05-15', 'Los Angeles', 500000),
('VCT Americas Stage 2', 'Americas', '2026-06-01', '2026-07-20', 'Los Angeles', 500000),
('VCT EMEA Stage 1', 'EMEA', '2026-04-03', '2026-05-14', 'Berlín', 500000),
('VCT Pacific Stage 1', 'Pacific', '2026-04-05', '2026-05-17', 'Seúl', 500000),
('VCT CN Stage 1', 'China', '2026-04-04', '2026-05-16', 'Shanghái', 500000),
('VALORANT Masters Bangkok', 'Internacional', '2026-03-05', '2026-03-22', 'Bangkok', 1000000),
('VALORANT Champions 2026', 'Internacional', '2026-08-10', '2026-08-30', 'París', 2250000);
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
('AG01', 'Jett', 'R01'),       -- Original 1
('AG02', 'Viper', 'R02'),      -- Original 2
('AG03', 'Raze', 'R01'),       -- Original 3
('AG04', 'Omen', 'R02'),       -- Original 4
('AG05', 'Astra', 'R02'),
('AG06', 'Breach', 'R03'),
('AG07', 'Brimstone', 'R02'),
('AG08', 'Chamber', 'R04'),
('AG09', 'Clove', 'R02'),
('AG10', 'Cypher', 'R04'),
('AG11', 'Deadlock', 'R04'),
('AG12', 'Fade', 'R03'),
('AG13', 'Gekko', 'R03'),
('AG14', 'Killjoy', 'R04'),    
('AG15', 'Harbor', 'R02'),
('AG16', 'Iso', 'R01'),
('AG17', 'KAY/O', 'R03'),
('AG18', 'Neon', 'R01'),
('AG19', 'Phoenix', 'R01'),
('AG20', 'Reyna', 'R01'),
('AG21', 'Sage', 'R04'),
('AG22', 'Skye', 'R03'),
('AG23', 'Sova', 'R03'),
('AG24', 'Tejo', 'R03'),
('AG25', 'Veto', 'R04'),
('AG26', 'Vyse', 'R04'),
('AG27', 'Waylay', 'R01'),
('AG28', 'Yoru', 'R01');

-- Habilidades
INSERT INTO Habilidad (Id_Habilidad, Nombre_Habilidad, Tecla, Dano, Cargas, Tiempo_de_activacion, Id_UltimateFK) VALUES
('H01', 'Impulso/Viento de Cola', 'E', 0, 1, 0.1, 'U01'), -- Jett
('H02', 'Nube Venenosa', 'Q', 0, 1, 0.5, 'U02'),          -- Viper
('H03', 'Balas de Pintura', 'E', 55, 1, 0.5, 'U03'),      -- Raze
('H04', 'Paranoia', 'Q', 0, 1, 0.5, 'U04'),               -- Omen
('H05', 'Pulso Nova', 'Q', 0, 1, 0.5, 'U05'),             -- Astra
('H06', 'Línea de Falla', 'E', 0, 1, 1.0, 'U06'),         -- Breach
('H07', 'Cortina de Humo', 'E', 0, 3, 0.5, 'U07'),        -- Brimstone
('H08', 'Marca Registrada', 'C', 0, 1, 0.8, 'U08'),       -- Chamber
('H09', 'Artimaña', 'E', 0, 2, 0.5, 'U09'),               -- Clove
('H10', 'Prisión Ciber', 'Q', 0, 2, 0.1, 'U10'),          -- Cypher
('H11', 'Malla de Barrera', 'E', 0, 1, 0.5, 'U11'),       -- Deadlock
('H12', 'Trampa', 'E', 0, 1, 0.7, 'U12'),                 -- Fade
('H13', 'Carnalito', 'Q', 0, 1, 0.5, 'U13'),              -- Gekko
('H14', 'Torreta', 'E', 11, 1, 0.8, 'U14'),               -- Killjoy
('H15', 'Marea Alta', 'E', 0, 1, 0.5, 'U15'),             -- Harbor
('H16', 'Flujo', 'E', 0, 1, 0.2, 'U16'),                  -- Iso
('H17', 'PUNTO/Cero', 'E', 0, 1, 0.5, 'U17'),             -- KAY/O
('H18', 'Velocidad Relámpago', 'E', 0, 1, 0.1, 'U18'),     -- Neon
('H19', 'Combustión', 'E', 60, 1, 0.5, 'U19'),            -- Phoenix
('H20', 'Devorar', 'Q', 0, 2, 0.1, 'U20'),                -- Reyna
('H21', 'Orbe de Barrera', 'C', 0, 1, 0.5, 'U21'),        -- Sage
('H22', 'Luz Guía', 'E', 0, 2, 0.3, 'U22'),               -- Skye
('H23', 'Proyectil de Reconocimiento', 'E', 0, 1, 0.5, 'U23'), -- Sova
('H24', 'Fuego Cruzado', 'E', 50, 1, 0.8, 'U24'),         -- Tejo
('H25', 'Línea de Bloqueo', 'E', 0, 1, 0.5, 'U25'),       -- Veto
('H26', 'Rosa de Cizalla', 'E', 0, 1, 0.5, 'U26'),        -- Vyse
('H27', 'Carga Crucial', 'E', 40, 2, 0.4, 'U27'),         -- Waylay
('H28', 'Infiltración', 'E', 0, 2, 0.5, 'U28');           -- Yoru

-- Partidas
INSERT INTO Partida (Id_Partida, fecha, Fase, Id_TorneoFK) VALUES
('P01', '2026-04-10', 1, 'T01'),
('P02', '2026-04-12', 1, 'T01'),
('P03', '2026-04-15', 1, 'T01');

-- Jugadores
INSERT INTO Jugador (Id_Player, Nombre, Pais, Agente, Id_Equipo) VALUES
('J01', 'Keznit', 'Chile', 'AG03', 'E01'),
('J02', 'Melser', 'Chile', 'AG04', 'E01'),
('J03', 'Aspas', 'Brasil', 'AG01', 'E02'),
('J04', 'Mazino', 'Chile', 'AG04', 'E02'),
('J05', 'Less', 'Brasil', 'AG02', 'E03'),
('J06', 'TenZ', 'Canadá', 'AG01', 'E04'),
('J07', 'Zellsis', 'Estados Unidos', 'AG04', 'E04'),
('J08', 'Asuna', 'Estados Unidos', 'AG03', 'E05'),
('J09', 'Cryocells', 'Estados Unidos', 'AG01', 'E05'),
('J10', 'eeiu', 'Canadá', 'AG03', 'E11');

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
('P01', 'E02', TRUE),
('P03', 'E04', TRUE),
('P03', 'E05', FALSE);

-- Partido_Equipo (P02: LOUD vs KRU, gana LOUD)
INSERT INTO Partido_Equipo (Id_PartidaFK, Id_EquipoFK, Indicador_victoria) VALUES
('P02', 'E03', TRUE),
('P02', 'E01', FALSE);

-- Estadistica_Partida
INSERT INTO Estadistica_Partida (ID_Estadistica, Puntuacion_equipo1, Puntuacion_equipo2, Duracion, Id_PartidaFK, Id_MapaFK) VALUES
('EP01', 11, 13, '00:45:00', 'P01', 'M01'),
('EP02', 13, 9, '00:38:00', 'P02', 'M02'),
('EP03', 13, 10, '00:51:12', 'P03', 'M10');

-- Estadistica_Jugador (Kills, Deaths, Assists)
INSERT INTO Estadistica_Jugador (Id_estadistica_jugador, kills, death, assists, Id_PlayerFK, Id_AgenteFK, Id_Partido) VALUES
-- Partida 1: KRU vs LEV
('EJ01', 25, 18, 5, 'J01', 'AG03', 'P01'), -- Keznit
('EJ02', 28, 15, 4, 'J03', 'AG01', 'P01'), -- Aspas
('EJ03', 12, 16, 15, 'J04', 'AG04', 'P01'), -- Mazino

-- Partida 2: LOUD vs KRU
('EJ04', 22, 14, 8, 'J05', 'AG02', 'P02'), -- Less
('EJ05', 18, 19, 6, 'J01', 'AG03', 'P02'), -- Keznit

('EJ06', 29, 12, 6, 'J06', 'AG01', 'P03'), -- TenZ con Jett
('EJ07', 15, 14, 18, 'J07', 'AG04', 'P03'), -- Zellsis 
('EJ08', 21, 18, 4, 'J08', 'AG03', 'P03');
-- Uso_Armas_Jugador
INSERT INTO Uso_Armas_Jugador (Id_Uso_Arma, Id_estadistica_jugadorFK, Id_ArmaFK, Kills_con_arma, Dano_con_arma) VALUES
('UA01', 'EJ01', 'A01', 20, 3000), -- Keznit Vandal
('UA02', 'EJ02', 'A03', 15, 2250); -- Aspas Operator
