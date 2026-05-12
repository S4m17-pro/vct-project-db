class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Conectar el botón de la vista con la función del controlador
        self.view.btn_consultar.configure(command=self.cargar_datos_vct)

    def cargar_datos_vct(self):
        # El controlador le pide al modelo los datos
        datos = self.model.obtener_vista_jugadores()
        # El controlador le pasa los datos a la vista para que los pinte
        self.view.actualizar_datos(datos)