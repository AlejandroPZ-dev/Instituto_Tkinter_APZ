import customtkinter as ctk

class HomePantalla(ctk.CTkFrame):
    def __init__(self, master, session):
        super().__init__(master)

        titulo = ctk.CTkLabel(
            self,
            text=f"Inicio - Bienvenido {session.get('username', 'usuario')}",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        titulo.pack(anchor="w", padx=18, pady=(18, 6))

        texto = ctk.CTkLabel(
            self,
            text="Desde el menú podrás entrar en Alumnos, Aulas, etc.\n\n"
                 "En este paso estamos aprendiendo a cargar pantallas dentro del contenido.",
            justify="left",
        )
        texto.pack(anchor="w", padx=18, pady=(0, 18))
