import psycopg2

class DatabaseManager:
    def __init__(self):
        self.config = {
            "dbname": "vct_stats",
            "user": "usuario_consulta",
            "password": "consulta123",
            "host": "localhost",
            "port": "5432"
        }

    def obtener_vista_jugadores(self):
        """Consulta la vista de ranking de jugadores"""
        try:
            conn = psycopg2.connect(**self.config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Vista_Resumen_Jugadores ORDER BY KDA DESC;")
            datos = cursor.fetchall()
            cursor.close()
            conn.close()
            return datos
        except Exception as e:
            print(f"Error al obtener vista de jugadores: {e}")
            return []

    def obtener_stats_equipos(self):
        """Consulta la vista de estadísticas por equipo"""
        try:
            conn = psycopg2.connect(**self.config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Vista_Estadisticas_Equipos;")
            datos = cursor.fetchall()
            cursor.close()
            conn.close()
            return datos
        except Exception as e:
            print(f"Error al obtener stats de equipos: {e}")
            return []

    def registrar_partida(self, id_p, fase, id_t, id_m, s1, s2, dur):
        """Llama al procedimiento almacenado para registrar una partida"""
        try:
            conn = psycopg2.connect(**self.config)
            cursor = conn.cursor()
            # Llamada al procedimiento almacenado sp_registrar_partida
            cursor.execute("CALL sp_registrar_partida(%s, %s, %s, %s, %s, %s, %s);", 
                         (id_p, fase, id_t, id_m, s1, s2, dur))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al ejecutar procedimiento: {e}")
            return False