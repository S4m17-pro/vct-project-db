# Manual de Administración de Base de Datos - VCT Stats

**Fecha de Entrega:** Primera Semana de Junio 2026
**Institución:** Universidad Libre
**Proyecto:** Sistema de Gestión y Estadísticas VCT

> [!TIP]
> **Instrucciones para generar el PDF:**
> Para cumplir con el requerimiento de entrega en PDF, puedes usar Visual Studio Code instalando la extensión **"Markdown PDF"** (creada por yzane). Una vez instalada, haz clic derecho sobre este archivo y selecciona `Markdown PDF: Export (pdf)`.

---

## Introducción

Este documento detalla el diseño, estructura y funcionamiento de la base de datos `vct_stats` para el aplicativo de gestión de torneos de Valorant. El aplicativo cuenta con una interfaz construida en Python (`customtkinter`) conectada directamente a una instancia PostgreSQL desplegada mediante Docker, garantizando un entorno aislado y profesional.

El aplicativo permite, de forma funcional y altamente estética, consultar los Rankings de Jugadores (con cálculos precisos de KDA) y las Estadísticas Generales de los Equipos (Victorias, Derrotas y Partidas Totales).

---

## 0. Diseño de la Base de Datos

La base de datos sigue un modelo relacional estrictamente normalizado para garantizar la integridad referencial. Está estructurada en distintos niveles de dependencia:

1. **Nivel 1 (Tablas Independientes):** Entidades base que no dependen de otras.
   - `Rol`: Roles de los agentes dentro del juego.
   - `Ultimate`, `Arma`, `Mapa`, `Torneo`, `Equipo`.
2. **Nivel 2 (Tablas con Dependencias):**
   - `Agente`: Vincula un agente con su `Rol`.
   - `Habilidad`: Relacionada con la tabla `Ultimate`.
   - `Partida`: Vinculada al `Torneo`.
   - `Jugador`: Clave foránea hacia `Equipo` y `Agente`.
3. **Nivel 3 (Tablas Transaccionales y Estadísticas):**
   - `Agente_Habilidad`: Tabla puente para relación N:M.
   - `Partido_Equipo`: Registra la participación de los equipos en las partidas y su indicador de victoria.
   - `Estadistica_Partida`: Duración, puntuaciones y mapa jugado.
   - `Estadistica_Jugador`: Kills, deaths, assists (KDA) por partida.
   - `Uso_Armas_Jugador`: Daño y kills por arma.
4. **Nivel 4 (Auditoría):**
   - `Audit_Log`: Tabla dedicada al registro de operaciones (INSERT, UPDATE, DELETE) generadas por los triggers.

---

## 1. Usuario de Base de Datos

Se han diseñado perfiles de acceso específicos basándose en el principio de mínimo privilegio (Seguridad y Buenas Prácticas PostgreSQL):

- **`usuario_consulta`**: Perfil utilizado por la interfaz gráfica de Python. Tiene permisos restrictivos (`GRANT CONNECT`, `GRANT USAGE ON SCHEMA`, `GRANT SELECT`) exclusivamente de lectura para todas las tablas. No puede alterar los datos, garantizando la seguridad de la información mostrada.
- **`usuario_editor`**: Perfil con privilegios CRUD (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) diseñado para administradores del sistema o futuras integraciones de backend que requieran modificar datos.
- **`lewis` (Colaborador)**: Usuario específico que, mediante políticas de *Default Privileges*, puede leer, insertar y alterar secuencias o procedimientos, ideal para desarrollo colaborativo.

---

## 2. Vistas

Se crearon tres (3) vistas fundamentales para pre-calcular métricas y facilitar su ingesta desde el aplicativo Python sin sobrecargar la red con joins innecesarios:

1. **`Vista_Resumen_Jugadores`**
   - **Explicación**: Une las tablas `Jugador`, `Equipo`, `Agente` y `Estadistica_Jugador`. Realiza el cálculo matemático en tiempo real del **KDA** (Kills + Assists / Deaths), protegiendo la división entre cero usando la función `GREATEST(ej.death, 1)`.
   - **Uso**: Alimenta la sección "Ranking Jugadores" en la interfaz gráfica.

2. **`Vista_Estadisticas_Equipos`**
   - **Explicación**: Agrupa la información de la tabla `Equipo` cruzándola con `Partido_Equipo`. Utiliza conteos condicionales (`COUNT(CASE WHEN...)`) para calcular total de partidas, victorias y derrotas por organización.
   - **Uso**: Alimenta la sección "Stats Equipos" en el Dashboard.

3. **`Vista_Detalles_Partida`**
   - **Explicación**: Compila un resumen legible (sin mostrar IDs crudos) del torneo, mapa, score del equipo 1, score del equipo 2, y la fecha, cruzando `Partida`, `Torneo`, `Estadistica_Partida` y `Mapa`.

---

## 3. Procedimientos Almacenados

La lógica transaccional compleja se ha delegado al motor de base de datos para asegurar el principio ACID:

- **`sp_registrar_partida(id_p, fase, id_t, id_m, s1, s2, dur)`**
  - **Explicación**: Este procedimiento encapsula la lógica para registrar una nueva partida en el circuito VCT. Realiza dos inserciones en bloque:
    1. Crea el registro principal en la tabla `Partida` (asignando el Torneo y la Fase).
    2. Crea simultáneamente el registro en `Estadistica_Partida` (asignando el Mapa, Puntuaciones y Duración).
  - Al estar en un procedimiento almacenado y ser llamado desde Python con manejadores de contexto (Context Managers de `psycopg2`), cualquier error revierte automáticamente la transacción (Rollback), evitando datos huérfanos.

- **`sp_actualizar_kda_jugador`**
  - **Explicación**: Un procedimiento auxiliar previsto para actualizar de forma atómica y masiva las estadísticas individuales (Kills, Deaths, Assists) de un jugador en particular tras finalizar una partida.

---

## 4. Triggers (Disparadores)

Se diseñaron triggers para control y auditoría automatizada sin depender del código fuente de la aplicación:

1. **`trg_auditoria_jugador` (Audit Log)**
   - **Explicación**: Se dispara `AFTER INSERT OR UPDATE OR DELETE` sobre la tabla `Jugador`. Llama a la función `fn_audit_jugador()`.
   - **Funcionalidad**: Detecta qué operación matemática ocurrió y escribe un log en la tabla `Audit_Log` capturando: Tabla Afectada, Operación (`TG_OP`), Usuario de la BD actual (`CURRENT_USER`) y el detalle del cambio (ej. nombre modificado).

2. **`trg_validar_puntuacion` (Validación de Integridad)**
   - **Explicación**: Se dispara `BEFORE INSERT OR UPDATE` sobre la tabla `Estadistica_Partida`. Llama a la función `fn_validar_puntaje()`.
   - **Funcionalidad**: Protege la integridad de los datos evaluando que ni el equipo 1 ni el equipo 2 puedan tener puntuaciones negativas. Si las tienen, levanta una excepción (`RAISE EXCEPTION`) y aborta la transacción inmediatamente a nivel de motor.
