import customtkinter as ctk

# Configuración global del tema siguiendo el minimalismo y elegancia
ctk.set_appearance_mode("Dark")  # Tema oscuro profundo
ctk.set_default_color_theme("dark-blue")  # Tema base, sobrescribiremos colores

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("VCT Stats - Universidad Libre")
        self.geometry("1000x600")
        self.minsize(800, 500)
        
        # Grid Layout: 1 fila, 2 columnas (Sidebar y Contenido)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) # El área principal se expande
        
        # Definición de paleta de colores profesional
        self.bg_color = "#09090b"        # Zinc-950 (Fondo principal)
        self.sidebar_color = "#18181b"   # Zinc-900 (Fondo sidebar)
        self.card_color = "#27272a"      # Zinc-800 (Fondo tarjetas)
        self.accent_color = "#ff4655"    # Rojo Valorant VCT (Acento)
        self.accent_hover = "#d43a47"
        self.text_primary = "#f4f4f5"    # Zinc-50
        self.text_secondary = "#a1a1aa"  # Zinc-400
        
        self.configure(fg_color=self.bg_color)
        
        self._build_sidebar()
        self._build_main_area()

    def _build_sidebar(self):
        # Frame del Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=self.sidebar_color)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Empuja hacia arriba
        
        # Logo / Título del Sidebar
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="VCT STATS\nUNIVERSIDAD LIBRE", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=self.text_primary
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 30))
        
        # Separador visual
        self.separator = ctk.CTkFrame(self.sidebar_frame, height=2, fg_color=self.card_color)
        self.separator.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Botones de navegación
        self.btn_consultar = ctk.CTkButton(
            self.sidebar_frame, 
            text="Ranking Jugadores", 
            fg_color="transparent", 
            text_color=self.text_secondary,
            hover_color=self.card_color,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=14)
        )
        self.btn_consultar.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        self.btn_equipos = ctk.CTkButton(
            self.sidebar_frame, 
            text="Stats Equipos", 
            fg_color="transparent", 
            text_color=self.text_secondary,
            hover_color=self.card_color,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=14)
        )
        self.btn_equipos.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        # Separador visual secundario
        self.separator2 = ctk.CTkFrame(self.sidebar_frame, height=2, fg_color=self.card_color)
        self.separator2.grid(row=4, column=0, sticky="ew", padx=20, pady=10)

        # Boton registrar (Accion)
        self.btn_registrar = ctk.CTkButton(
            self.sidebar_frame, 
            text="Registrar Partida", 
            fg_color="transparent", 
            text_color=self.text_secondary,
            hover_color=self.card_color,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        )
        self.btn_registrar.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

    def _build_main_area(self):
        # Frame del Área Principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Título del contexto actual
        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text="Panel de Control", 
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=self.text_primary,
            anchor="w"
        )
        self.header_label.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        # Scrollable Frame para simular una tabla de datos/DataGrid
        self.data_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent", corner_radius=0)
        self.data_frame.grid(row=1, column=0, sticky="nsew")
        self.data_frame.grid_columnconfigure(0, weight=1)
        
        # Mensaje por defecto
        self._mostrar_mensaje_vacio("Selecciona una opción en el menú lateral.")

    def _limpiar_datos(self):
        for widget in self.data_frame.winfo_children():
            widget.destroy()

    def _mostrar_mensaje_vacio(self, texto):
        self._limpiar_datos()
        label = ctk.CTkLabel(
            self.data_frame, 
            text=texto, 
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=self.text_secondary
        )
        label.grid(row=0, column=0, pady=100)

    def set_active_menu(self, btn_activo):
        # Restablece estilos de botones inactivos
        for btn in [self.btn_consultar, self.btn_equipos, self.btn_registrar]:
            btn.configure(fg_color="transparent", text_color=self.text_secondary)
        # Aplica estilo de botón activo
        btn_activo.configure(fg_color=self.accent_color, text_color=self.text_primary, hover_color=self.accent_hover)

    def mostrar_vista_jugadores(self, datos):
        self.set_active_menu(self.btn_consultar)
        self.header_label.configure(text="Ranking de Jugadores")
        self._limpiar_datos()
        
        if not datos:
            self._mostrar_mensaje_vacio("No hay datos disponibles.")
            return

        # Renderizar cada fila como una tarjeta elegante
        for i, fila in enumerate(datos):
            jugador = fila[0]
            equipo = fila[1]
            agente = fila[2]
            kda = fila[6] # Indice 6 es KDA basado en la vista SQL (Nombre, Equipo, Agente, kills, death, assists, KDA)
            
            card = ctk.CTkFrame(self.data_frame, fg_color=self.card_color, corner_radius=8)
            card.grid(row=i, column=0, sticky="ew", pady=5, padx=5)
            card.grid_columnconfigure(0, weight=1)
            card.grid_columnconfigure(1, weight=0)
            
            # Contenedor izquierdo: Jugador y Equipo
            left_frame = ctk.CTkFrame(card, fg_color="transparent")
            left_frame.grid(row=0, column=0, sticky="w", padx=20, pady=15)
            
            name_label = ctk.CTkLabel(left_frame, text=f"{jugador}", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color=self.text_primary)
            name_label.grid(row=0, column=0, sticky="w")
            
            subtitle = ctk.CTkLabel(left_frame, text=f"{equipo}  •  {agente}", font=ctk.CTkFont(family="Segoe UI", size=12), text_color=self.text_secondary)
            subtitle.grid(row=1, column=0, sticky="w")
            
            # Contenedor derecho: KDA Metric
            right_frame = ctk.CTkFrame(card, fg_color="transparent")
            right_frame.grid(row=0, column=1, sticky="e", padx=20, pady=15)
            
            kda_value_label = ctk.CTkLabel(right_frame, text=f"{kda}", font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"), text_color=self.accent_color)
            kda_value_label.grid(row=0, column=0, sticky="e")
            kda_title_label = ctk.CTkLabel(right_frame, text="KDA", font=ctk.CTkFont(family="Segoe UI", size=10), text_color=self.text_secondary)
            kda_title_label.grid(row=1, column=0, sticky="e")

    def mostrar_vista_equipos(self, datos):
        self.set_active_menu(self.btn_equipos)
        self.header_label.configure(text="Estadísticas de Equipos")
        self._limpiar_datos()
        
        if not datos:
            self._mostrar_mensaje_vacio("No hay datos disponibles.")
            return

        for i, fila in enumerate(datos):
            nombre_equipo = fila[0]
            partidas = fila[1]
            victorias = fila[2]
            derrotas = fila[3]
            
            # Tarjeta de Equipo
            card = ctk.CTkFrame(self.data_frame, fg_color=self.card_color, corner_radius=8)
            card.grid(row=i, column=0, sticky="ew", pady=5, padx=5)
            
            card.grid_columnconfigure(0, weight=1)
            card.grid_columnconfigure(1, weight=1)
            card.grid_columnconfigure(2, weight=1)
            card.grid_columnconfigure(3, weight=1)
            
            # Nombre de Equipo (Izquierda)
            name_label = ctk.CTkLabel(card, text=nombre_equipo, font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color=self.text_primary, anchor="w")
            name_label.grid(row=0, column=0, sticky="w", padx=20, pady=20)
            
            # Métricas
            def create_metric(parent, label, value, col):
                f = ctk.CTkFrame(parent, fg_color="transparent")
                f.grid(row=0, column=col, sticky="e", padx=20, pady=10)
                v_label = ctk.CTkLabel(f, text=str(value), font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color=self.text_primary)
                v_label.grid(row=0, column=0)
                t_label = ctk.CTkLabel(f, text=label, font=ctk.CTkFont(family="Segoe UI", size=10), text_color=self.text_secondary)
                t_label.grid(row=1, column=0)
            
            create_metric(card, "Partidas", partidas, 1)
            create_metric(card, "Victorias", victorias, 2)
            create_metric(card, "Derrotas", derrotas, 3)

    def mostrar_vista_registro(self, torneos, mapas, equipos, callback_submit):
        self.set_active_menu(self.btn_registrar)
        self.header_label.configure(text="Registrar Nueva Partida")
        self._limpiar_datos()

        # Contenedor del formulario centralizado
        form_frame = ctk.CTkFrame(self.data_frame, fg_color=self.card_color, corner_radius=12)
        form_frame.grid(row=0, column=0, pady=20, padx=50, sticky="ew")
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        inputs = {}
        
        # Helper para crear inputs limpios
        def create_input(row, label_text, key, placeholder, col=0):
            lbl = ctk.CTkLabel(form_frame, text=label_text, font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=self.text_secondary)
            lbl.grid(row=row, column=col, sticky="w", padx=20, pady=(15, 0))
            entry = ctk.CTkEntry(form_frame, placeholder_text=placeholder, fg_color=self.bg_color, border_color=self.sidebar_color, text_color=self.text_primary, height=40)
            entry.grid(row=row+1, column=col, sticky="ew", padx=20, pady=(5, 10))
            inputs[key] = entry
            
        # Helper para crear selects limpios
        def create_select(row, label_text, key, values, col=0):
            lbl = ctk.CTkLabel(form_frame, text=label_text, font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=self.text_secondary)
            lbl.grid(row=row, column=col, sticky="w", padx=20, pady=(15, 0))
            # Prevenir error si la lista está vacía
            combo_values = values if values else ["Sin datos"]
            combo = ctk.CTkComboBox(form_frame, values=combo_values, fg_color=self.bg_color, border_color=self.sidebar_color, text_color=self.text_primary, height=40, dropdown_fg_color=self.bg_color)
            combo.grid(row=row+1, column=col, sticky="ew", padx=20, pady=(5, 10))
            inputs[key] = combo

        # Fila 1
        create_input(0, "ID Partida (Ej: P03)", "id_p", "P0X", 0)
        create_input(0, "Fase (Ej: 1)", "fase", "1", 1)
        
        # Fila 2
        create_select(2, "Torneo", "torneo", torneos, 0)
        create_select(2, "Mapa", "mapa", mapas, 1)
        
        # Fila 3
        create_select(4, "Equipo 1", "equipo1", equipos, 0)
        create_select(4, "Equipo 2", "equipo2", equipos, 1)
        
        # Fila 4
        create_input(6, "Score Equipo 1", "s1", "13", 0)
        create_input(6, "Score Equipo 2", "s2", "11", 1)

        # Fila 5
        create_input(8, "Duración (HH:MM:SS)", "dur", "00:45:00", 0)

        # Error label
        self.error_label = ctk.CTkLabel(form_frame, text="", text_color=self.accent_color, font=ctk.CTkFont(family="Segoe UI", size=12))
        self.error_label.grid(row=10, column=0, columnspan=2, pady=(10, 0))

        # Submit button
        def on_submit():
            data = {k: v.get() for k, v in inputs.items()}
            callback_submit(data)

        btn_submit = ctk.CTkButton(
            form_frame, text="GUARDAR PARTIDA", 
            fg_color=self.accent_color, hover_color=self.accent_hover,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=45, command=on_submit
        )
        btn_submit.grid(row=11, column=0, columnspan=2, sticky="ew", padx=20, pady=20)

    def mostrar_alerta(self, mensaje, exito=True):
        if hasattr(self, 'error_label') and self.error_label.winfo_exists():
            color = "#10b981" if exito else self.accent_color # Verde emerald para exito
            self.error_label.configure(text=mensaje, text_color=color)
            # Limpiar entradas si es exito
            if exito:
                for widget in self.data_frame.winfo_children():
                    if isinstance(widget, ctk.CTkFrame):
                        for child in widget.winfo_children():
                            if isinstance(child, ctk.CTkEntry):
                                child.delete(0, 'end')
