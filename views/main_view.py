import customtkinter as ctk
from tkinter import messagebox

from views.pantallas.alumnos_pantalla import AlumnosPantalla
from views.pantallas.aulas_pantalla import AulasPantalla
from views.pantallas.home_pantalla import HomePantalla
from views.pantallas.profesores_pantalla import ProfesoresPantalla


class MainView(ctk.CTkFrame):
    def __init__(self, master, session):
        super().__init__(master)

        # Info de sesión (usuario, rol, etc.)
        self.session = session

        # Pantalla actual cargada en el área de contenido
        self.current_screen = None

        # Guardaremos botones del menú para poder marcar cuál está activo
        self.menu_buttons = {}

        # Definimos rutas (qué pantalla corresponde a cada opción)
        self.routes = {
            "Inicio": lambda: HomePantalla(self.content, session=self.session),
            "Alumnos": lambda: AlumnosPantalla(self.content),
            "Aulas": lambda: AulasPantalla(self.content),
            "Profesores": lambda: ProfesoresPantalla(self.content),
        }

        self._build_topbar()
        self._build_body()

        # Mostrar pantalla inicial
        self._show_section("Inicio")

    def _build_topbar(self):
        # Barra superior
        self.topbar = ctk.CTkFrame(self, corner_radius=0)
        self.topbar.pack(side="top", fill="x")

        self.welcome_label = ctk.CTkLabel(
            self.topbar,
            text=f"Bienvenido, {self.session.get('username', 'usuario')}",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.welcome_label.pack(side="left", padx=16, pady=12)

        self.exit_btn = ctk.CTkButton(self.topbar, text="Salir", command=self._confirm_exit)
        self.exit_btn.pack(side="right", padx=16, pady=12)

    def _build_body(self):
        # Cuerpo principal (menú + contenido)
        self.body = ctk.CTkFrame(self, corner_radius=0)
        self.body.pack(side="top", fill="both", expand=True)

        # Menú lateral
        self.sidebar = ctk.CTkFrame(self.body, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="Menú",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        sidebar_title.pack(pady=(16, 8))

        # Botones del menú
        for name in ["Inicio", "Alumnos", "Profesores", "Aulas", "Materiales", "Asignaturas", "Clases", "Calificaciones"]:
            self._add_menu_button(name)

        # Área de contenido (aquí se cargan las pantallas)
        self.content = ctk.CTkFrame(self.body, corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

    def _add_menu_button(self, name: str):
        # Creamos el botón y lo guardamos en un diccionario
        btn = ctk.CTkButton(
            self.sidebar,
            text=name,
            command=lambda n=name: self._show_section(n)
        )
        btn.pack(padx=12, pady=6, fill="x")
        self.menu_buttons[name] = btn

    def _show_section(self, name: str):
        # Destruimos la pantalla anterior
        if self.current_screen is not None:
            self.current_screen.destroy()
            self.current_screen = None

        # Marcamos el botón activo (visual)
        self._set_active_menu_button(name)

        # Creamos la pantalla usando rutas si existe
        if name in self.routes:
            self.current_screen = self.routes[name]()
        else:
            # Pantalla por defecto si no está implementada
            self.current_screen = ctk.CTkFrame(self.content)
            label = ctk.CTkLabel(self.current_screen, text=f"Pantalla '{name}' no implementada.")
            label.pack(padx=18, pady=18, anchor="w")

        # Mostramos la pantalla
        self.current_screen.pack(fill="both", expand=True)

    def _set_active_menu_button(self, active_name: str):
        # Dejamos todos los botones en estado normal
        for name, btn in self.menu_buttons.items():
            btn.configure(state="normal")

        # Truco simple: deshabilitamos el botón activo para que se vea "seleccionado"
        # (Más adelante se puede mejorar con estilos/colores)
        if active_name in self.menu_buttons:
            self.menu_buttons[active_name].configure(state="disabled")

    def _confirm_exit(self):
        if messagebox.askyesno("Salir", "¿Seguro que quieres cerrar la aplicación?"):
            self.master.destroy()
