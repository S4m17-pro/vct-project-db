class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Conectar los botones de la vista con las funciones del controlador
        self.view.btn_consultar.configure(command=self.cargar_datos_vct)
        self.view.btn_equipos.configure(command=self.cargar_stats_equipos)

    def cargar_datos_vct(self):
        # El controlador le pide al modelo los datos de la vista de jugadores
        datos = self.model.obtener_vista_jugadores()
        self.view.actualizar_datos(datos)

    def cargar_stats_equipos(self):
        # El controlador le pide al modelo los datos de la vista de equipos
        datos = self.model.obtener_stats_equipos()
        # Formateamos los datos para la vista
        texto_final = []
        for fila in datos:
            texto_final.append(f"EQUIPO: {fila[0]} | PARTIDAS: {fila[1]} | VICTORIAS: {fila[2]} | DERROTAS: {fila[3]}")
        
        self.view.textbox.delete("0.0", "end")
        self.view.textbox.insert("end", "\n".join(texto_final))