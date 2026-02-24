import customtkinter as ctk
from views.login_view import LoginView
from views.main_view import MainView

def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Instituto")
    app.geometry("900x600")

    current_frame = None

    def show_view(frame):
        nonlocal current_frame
        if current_frame is not None:
            current_frame.destroy()
        current_frame = frame
        frame.pack(fill="both", expand=True)

    def autenticar(usuario: str, clave: str):
        # Lógica provisional. Más adelante: AuthService + tabla usuario.
        if usuario == "admin" and clave == "admin":
            return {"username": usuario, "role": "ADMIN"}
        return None

    def ir_a_main(session):
        show_view(MainView(app, session=session))

    # Mostramos login
    show_view(LoginView(app, autenticar=autenticar, on_success=ir_a_main))
    app.mainloop()

if __name__ == "__main__":
    main()
