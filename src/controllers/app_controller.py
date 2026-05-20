class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Conectar los botones de la vista con las funciones del controlador
        self.view.btn_consultar.configure(command=self.cargar_datos_vct)
        self.view.btn_equipos.configure(command=self.cargar_stats_equipos)
        self.view.btn_registrar.configure(command=self.cargar_vista_registro)
        
        # Cargar datos de jugadores por defecto al iniciar la app para que no esté vacío
        # Utilizamos after para dar tiempo a que la ventana se inicialice completamente
        self.view.after(100, self.cargar_datos_vct)

    def cargar_datos_vct(self):
        # El controlador le pide al modelo los datos de la vista de jugadores
        datos = self.model.obtener_vista_jugadores()
        # Pasamos los datos crudos a la vista, la vista se encarga de presentarlos
        self.view.mostrar_vista_jugadores(datos)

    def cargar_stats_equipos(self):
        # El controlador le pide al modelo los datos de la vista de equipos
        datos = self.model.obtener_stats_equipos()
        # Pasamos los datos crudos a la vista
        self.view.mostrar_vista_equipos(datos)

    def cargar_vista_registro(self):
        # Muestra el formulario y le pasa la funcion callback que procesara el submit
        torneos = self.model.obtener_torneos()
        mapas = self.model.obtener_mapas()
        equipos = self.model.obtener_equipos()
        
        # Guardamos los mapeos invertidos para fácil traducción de string seleccionado -> ID crudo
        self.mapas_dict = torneos
        self.mapas_dict.update(mapas)
        self.mapas_dict.update(equipos)

        self.view.mostrar_vista_registro(
            list(torneos.keys()), 
            list(mapas.keys()), 
            list(equipos.keys()), 
            self.procesar_registro_partida
        )

    def procesar_registro_partida(self, datos_formulario):
        # Validar campos vacíos básicos
        for key, val in datos_formulario.items():
            if not val.strip():
                self.view.mostrar_alerta("Error: Todos los campos son obligatorios.", exito=False)
                return

        try:
            # Casteo de tipos para el procedimiento almacenado
            id_p = datos_formulario['id_p']
            fase = int(datos_formulario['fase'])
            # Resolviendo los IDs reales usando el diccionario global temporal
            id_t = self.mapas_dict.get(datos_formulario['torneo'])
            id_m = self.mapas_dict.get(datos_formulario['mapa'])
            id_e1 = self.mapas_dict.get(datos_formulario['equipo1'])
            id_e2 = self.mapas_dict.get(datos_formulario['equipo2'])
            
            s1 = int(datos_formulario['s1'])
            s2 = int(datos_formulario['s2'])
            dur = datos_formulario['dur']

            # Validacion simple score
            if s1 < 0 or s2 < 0:
                self.view.mostrar_alerta("Error: Los scores no pueden ser negativos.", exito=False)
                return

            exito = self.model.registrar_partida(id_p, fase, id_t, id_m, id_e1, id_e2, s1, s2, dur)
            
            if exito:
                self.view.mostrar_alerta("¡Partida registrada exitosamente!", exito=True)
            else:
                self.view.mostrar_alerta("Error al registrar en la Base de Datos.", exito=False)
                
        except ValueError:
            self.view.mostrar_alerta("Error: Fase y Scores deben ser números enteros.", exito=False)
        except Exception as e:
            self.view.mostrar_alerta(f"Error inesperado: {str(e)}", exito=False)