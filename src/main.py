import sys
import os

# Esto es para que Python encuentre las carpetas locales
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database_manager import DatabaseManager
from views.main_window import MainWindow
from controllers.app_controller import AppController

def main():
    # 1. Crear el Modelo
    modelo = DatabaseManager()
    
    # 2. Crear la Vista
    vista = MainWindow()
    
    # 3. Crear el Controlador y pasarle ambos
    AppController(modelo, vista)
    
    # 4. Iniciar la aplicación
    vista.mainloop()

if __name__ == "__main__":
    main()