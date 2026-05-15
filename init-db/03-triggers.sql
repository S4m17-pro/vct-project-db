-- ==========================================
-- 03-triggers.sql
-- Descripción: Disparadores para auditoría y validación
-- ==========================================

-- 1. Función y Trigger de Auditoría para la tabla Jugador
-- Registra quién cambió qué y cuándo
CREATE OR REPLACE FUNCTION fn_audit_jugador()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO Audit_Log (Tabla_Afectada, Operacion, Usuario, Detalle)
        VALUES ('Jugador', 'INSERT', CURRENT_USER, 'Nuevo jugador: ' || NEW.Nombre);
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO Audit_Log (Tabla_Afectada, Operacion, Usuario, Detalle)
        VALUES ('Jugador', 'UPDATE', CURRENT_USER, 'Cambio en ID ' || OLD.Id_Player || ': ' || OLD.Nombre || ' -> ' || NEW.Nombre);
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO Audit_Log (Tabla_Afectada, Operacion, Usuario, Detalle)
        VALUES ('Jugador', 'DELETE', CURRENT_USER, 'Eliminado jugador ID ' || OLD.Id_Player);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_auditoria_jugador
AFTER INSERT OR UPDATE OR DELETE ON Jugador
FOR EACH ROW EXECUTE FUNCTION fn_audit_jugador();

-- 2. Función y Trigger de Validación de Puntajes
-- Evita que se inserten puntuaciones negativas
CREATE OR REPLACE FUNCTION fn_validar_puntaje()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.Puntuacion_equipo1 < 0 OR NEW.Puntuacion_equipo2 < 0 THEN
        RAISE EXCEPTION 'La puntuación de los equipos no puede ser negativa.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validar_puntuacion
BEFORE INSERT OR UPDATE ON Estadistica_Partida
FOR EACH ROW EXECUTE FUNCTION fn_validar_puntaje();

-- 3. Trigger para Registrar Última Modificación (Opcional)
-- Si quisiéramos actualizar una columna 'ultima_actualizacion' automáticamente
-- Se puede aplicar a cualquier tabla que tenga esa columna
