import customtkinter as ctk

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VCT Stats - Universidad Libre")
        self.geometry("800x500")
        
        # Configuración de grid
        self.grid_columnconfigure(0, weight=1)
        
        # UI Elements
        self.label = ctk.CTkLabel(self, text="Panel de Control VCT", font=("Arial", 24, "bold"))
        self.label.grid(row=0, column=0, pady=20)

        self.btn_consultar = ctk.CTkButton(self, text="Cargar Estadísticas (View)", fg_color="#ff4655")
        self.btn_consultar.grid(row=1, column=0, pady=10)

        self.textbox = ctk.CTkTextbox(self, width=700, height=300)
        self.textbox.grid(row=2, column=0, padx=20, pady=20)

    def actualizar_datos(self, datos):
        self.textbox.delete("0.0", "end")
        for fila in datos:
            texto = f"JUGADOR: {fila[0]} | EQUIPO: {fila[1]} | KDA: {fila[2]}/{fila[3]}/{fila[4]}\n"
            self.textbox.insert("end", texto)