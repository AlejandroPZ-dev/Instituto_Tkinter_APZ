import customtkinter as ctk

class AulasPantalla(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        titulo = ctk.CTkLabel(
            self,
            text="Aulas",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        titulo.pack(anchor="w", padx=18, pady=(18, 6))

        texto = ctk.CTkLabel(
            self,
            text="Aquí irá el CRUD de aulas.\n\nPor ahora es una pantalla de prueba.",
            justify="left",
        )
        texto.pack(anchor="w", padx=18, pady=(0, 18))
