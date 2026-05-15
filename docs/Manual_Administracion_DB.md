# Manual de Administración de Base de Datos - VCT Stats

## 1. Introducción
Este aplicativo permite la gestión y visualización de estadísticas del circuito profesional de Valorant (VCT). La base de datos está diseñada en PostgreSQL y se despliega automáticamente mediante Docker.

## 2. Diseño de la Base de Datos (Modelo Relacional)
La base de datos `vct_stats` se compone de las siguientes entidades principales:
- **Equipos y Jugadores:** Almacena la información de las organizaciones y sus pro-players.
- **Torneos y Partidas:** Registra los eventos competitivos y los encuentros disputados.
- **Estadísticas:** Tablas dedicadas a Kills, Deaths, Assists y desempeño por mapa/arma.

> [!NOTE]
> El diseño sigue una estructura de niveles (1, 2 y 3) para garantizar la integridad referencial.

## 3. Vistas Diseñadas
Se implementaron 3 vistas para facilitar la consulta de información compleja:

1. **`Vista_Resumen_Jugadores`**: Calcula el KDA en tiempo real uniendo las tablas de jugadores y estadísticas.
2. **`Vista_Estadisticas_Equipos`**: Agrega el conteo de victorias y derrotas por cada organización.
3. **`Vista_Detalles_Partida`**: Proporciona un resumen legible de cada encuentro (Torneo, Mapa, Scores).

## 4. Procedimientos Almacenados
Los procedimientos permiten encapsular lógica de negocio directamente en el motor:

- **`sp_registrar_partida`**: Recibe los datos de un encuentro y realiza múltiples inserciones (Partida y Estadisticas) de forma atómica (usando transacciones `COMMIT`/`ROLLBACK`).
- **`sp_actualizar_kda_jugador`**: Facilita la actualización masiva de estadísticas individuales.

## 5. Triggers (Disparadores)
Automatismos para seguridad y auditoría:

- **`trg_auditoria_jugador`**: Cada vez que se inserta, edita o elimina un jugador, se registra el evento en la tabla `Audit_Log`, incluyendo el usuario que realizó la acción.
- **`trg_validar_puntuacion`**: Valida que no se ingresen scores negativos antes de realizar el insert en la tabla de estadísticas de partida.

## 6. Usuarios y Seguridad
Se han definido los siguientes roles:
- **`usuario_consulta`**: Solo lectura.
- **`usuario_editor`**: Permisos de CRUD sobre tablas.
- **`lewis`**: Usuario colaborador con permisos para ejecutar procedimientos y vistas.

---
**Fecha de Entrega:** Primera semana de Junio 2026
**Institución:** Universidad Libre
