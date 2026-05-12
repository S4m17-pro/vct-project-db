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
        """Consulta la vista creada en la base de datos"""
        try:
            conn = psycopg2.connect(**self.config)
            cursor = conn.cursor()
            # Usamos la vista del punto 2 de tu exigencia
            cursor.execute("SELECT * FROM Vista_Resumen_Jugadores;")
            datos = cursor.fetchall()
            cursor.close()
            conn.close()
            return datos
        except Exception as e:
            print(f"Error en el Modelo: {e}")
            return []