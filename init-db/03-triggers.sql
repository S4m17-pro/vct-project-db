-- ==========================================
-- 03-triggers.sql
-- Triggers para auditoría y validación
-- ==========================================

-- 1. Auditoría para Jugador (original)
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

DROP TRIGGER IF EXISTS trg_auditoria_jugador ON Jugador;
CREATE TRIGGER trg_auditoria_jugador
AFTER INSERT OR UPDATE OR DELETE ON Jugador
FOR EACH ROW EXECUTE FUNCTION fn_audit_jugador();

-- 2. Validación de Puntajes (original)
CREATE OR REPLACE FUNCTION fn_validar_puntaje()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.Puntuacion_equipo1 < 0 OR NEW.Puntuacion_equipo2 < 0 THEN
        RAISE EXCEPTION 'La puntuación de los equipos no puede ser negativa.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_validar_puntuacion ON Estadistica_Partida;
CREATE TRIGGER trg_validar_puntuacion
BEFORE INSERT OR UPDATE ON Estadistica_Partida
FOR EACH ROW EXECUTE FUNCTION fn_validar_puntaje();

-- 3. Auditoría para Equipo
CREATE OR REPLACE FUNCTION fn_audit_equipo()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO Audit_Log (Tabla_Afectada, Operacion, Usuario, Detalle)
        VALUES ('Equipo', 'INSERT', CURRENT_USER, 'Nuevo equipo: ' || NEW.Nombre_Equipo);
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO Audit_Log (Tabla_Afectada, Operacion, Usuario, Detalle)
        VALUES ('Equipo', 'UPDATE', CURRENT_USER, 'Cambio en ID ' || OLD.Id_Equipo || ': ' || OLD.Nombre_Equipo || ' -> ' || NEW.Nombre_Equipo);
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO Audit_Log (Tabla_Afectada, Operacion, Usuario, Detalle)
        VALUES ('Equipo', 'DELETE', CURRENT_USER, 'Eliminado equipo ID ' || OLD.Id_Equipo);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_auditoria_equipo ON Equipo;
CREATE TRIGGER trg_auditoria_equipo
AFTER INSERT OR UPDATE OR DELETE ON Equipo
FOR EACH ROW EXECUTE FUNCTION fn_audit_equipo();

-- 4. Auditoría para Partida
CREATE OR REPLACE FUNCTION fn_audit_partida()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO Audit_Log (Tabla_Afectada, Operacion, Usuario, Detalle)
        VALUES ('Partida', 'INSERT', CURRENT_USER, 'Nueva partida: ' || NEW.Id_Partida);
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO Audit_Log (Tabla_Afectada, Operacion, Usuario, Detalle)
        VALUES ('Partida', 'UPDATE', CURRENT_USER, 'Cambio en partida ' || OLD.Id_Partida);
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO Audit_Log (Tabla_Afectada, Operacion, Usuario, Detalle)
        VALUES ('Partida', 'DELETE', CURRENT_USER, 'Eliminada partida ID ' || OLD.Id_Partida);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_auditoria_partida ON Partida;
CREATE TRIGGER trg_auditoria_partida
AFTER INSERT OR UPDATE OR DELETE ON Partida
FOR EACH ROW EXECUTE FUNCTION fn_audit_partida();

-- 5. Validación KDA no negativo
CREATE OR REPLACE FUNCTION fn_validar_kda()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.kills < 0 OR NEW.death < 0 OR NEW.assists < 0 THEN
        RAISE EXCEPTION 'Kills, deaths y assists no pueden ser negativos.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_validar_kda ON Estadistica_Jugador;
CREATE TRIGGER trg_validar_kda
BEFORE INSERT OR UPDATE ON Estadistica_Jugador
FOR EACH ROW EXECUTE FUNCTION fn_validar_kda();

-- 6. Actualizar ultima_modificacion automáticamente
CREATE OR REPLACE FUNCTION fn_actualizar_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.ultima_modificacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_actualizar_mod_equipo ON Equipo;
CREATE TRIGGER trg_actualizar_mod_equipo
BEFORE UPDATE ON Equipo
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_modificacion();

DROP TRIGGER IF EXISTS trg_actualizar_mod_partida ON Partida;
CREATE TRIGGER trg_actualizar_mod_partida
BEFORE UPDATE ON Partida
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_modificacion();
