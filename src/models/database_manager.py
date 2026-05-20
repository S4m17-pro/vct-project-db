import psycopg2

class DatabaseManager:
    def __init__(self):
        self.config = {
            "dbname": "vct_stats",
            "user": "usuario_editor",  # Cambiado a usuario_editor para poder insertar registros
            "password": "editor123",
            "host": "localhost",
            "port": "5432"
        }

    def obtener_vista_jugadores(self):
        """Consulta la vista de ranking de jugadores"""
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cursor:
                    # Aplicando buenas prácticas: el ordenado se delega a la vista/DB
                    cursor.execute("SELECT * FROM Vista_Resumen_Jugadores ORDER BY KDA DESC;")
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener vista de jugadores: {e}")
            return []

    def obtener_stats_equipos(self):
        """Consulta la vista de estadísticas por equipo"""
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cursor:
                    # Utilizamos la vista ya definida
                    cursor.execute("SELECT * FROM Vista_Estadisticas_Equipos;")
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener stats de equipos: {e}")
            return []

    # --- MÉTODOS NUEVOS PARA SELECTS DINÁMICOS ---
    
    def obtener_torneos(self):
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT Id_Torneo, nombre_torneo FROM Torneo;")
                    return {f"{t[0]} - {t[1]}": t[0] for t in cursor.fetchall()}
        except Exception as e:
            print(f"Error al obtener torneos: {e}")
            return {}

    def obtener_mapas(self):
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT Id_Mapa, Nombre_Mapa FROM Mapa;")
                    return {f"{m[0]} - {m[1]}": m[0] for m in cursor.fetchall()}
        except Exception as e:
            print(f"Error al obtener mapas: {e}")
            return {}

    def obtener_equipos(self):
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT Id_Equipo, Nombre_Equipo FROM Equipo;")
                    return {f"{e[0]} - {e[1]}": e[0] for e in cursor.fetchall()}
        except Exception as e:
            print(f"Error al obtener equipos: {e}")
            return {}

    # ---------------------------------------------

    def registrar_partida(self, id_p, fase, id_t, id_m, id_e1, id_e2, s1, s2, dur):
        """Llama al procedimiento almacenado para registrar una partida"""
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cursor:
                    # Llamada segura al SP, delegando manejo de transacciones a Psycopg2 Context Manager
                    cursor.execute("CALL sp_registrar_partida(%s, %s, %s, %s, %s, %s, %s, %s, %s);", 
                                 (id_p, fase, id_t, id_m, id_e1, id_e2, s1, s2, dur))
                # Commit se hace automáticamente al salir del context manager si no hay excepción
            return True
        except Exception as e:
            print(f"Error al ejecutar procedimiento: {e}")
            return False