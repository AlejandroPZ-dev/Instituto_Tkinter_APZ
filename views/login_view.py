import customtkinter as ctk

class LoginView(ctk.CTkFrame):
    def __init__(self, master, autenticar, on_success):
        super().__init__(master)

        # Guardamos callbacks:
        # - autenticar(usuario, pass) -> devuelve session o None
        # - on_success(session) -> la app cambia de vista
        self.autenticar = autenticar
        self.on_success = on_success

        contenedor = ctk.CTkFrame(self, corner_radius=12)
        contenedor.pack(padx=20, pady=20, fill="both", expand=True)

        titulo = ctk.CTkLabel(
            contenedor,
            text="Acceso al Instituto",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.user_entry = ctk.CTkEntry(contenedor)
        titulo.pack(pady=(20, 10))

        self.user_entry = ctk.CTkEntry(contenedor, placeholder_text="Usuario")
        self.user_entry.pack(padx=30, pady=(10, 10), fill="x")

        # show="*" hace que la contraseña se vea como asteriscos
        self.pass_entry = ctk.CTkEntry(contenedor, placeholder_text="Contraseña", show="*")
        self.pass_entry.pack(padx=30, pady=(0, 10), fill="x")

        self.status_label = ctk.CTkLabel(contenedor, text="")
        self.status_label.pack(pady=(5, 0))

        self.login_btn = ctk.CTkButton(contenedor, text="Entrar", command=self._submit)
        self.login_btn.pack(padx=30, pady=(12, 20), fill="x")

        # Enter solo funciona dentro de los campos (no en toda la app)
        self.user_entry.bind("<Return>", lambda _e: self._submit())
        self.pass_entry.bind("<Return>", lambda _e: self._submit())

        self.user_entry.focus_set()

    def _submit(self):
        usuario = self.user_entry.get().strip()
        clave = self.pass_entry.get().strip()

        if not usuario or not clave:
            self._set_status("Introduce usuario y contraseña.")
            return

        self.login_btn.configure(state="disabled")
        self._set_status("Comprobando...")

        # Comprobamos credenciales (por ahora demo)
        session = self.autenticar(usuario, clave)

        if not session:
            self._set_status("Usuario o contraseña incorrectos.")
            self.login_btn.configure(state="normal")
            return

        # Programamos el cambio de vista para después de este callback.
        # Así evitamos tocar widgets ya destruidos.
        self._set_status("")
        self.after(0, lambda: self.on_success(session))

    def _set_status(self, msg: str):
        self.status_label.configure(text=msg)
