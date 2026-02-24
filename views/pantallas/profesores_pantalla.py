import customtkinter as ctk
from tkinter import messagebox

from db.db import (
    get_profesores,
    insert_profesor,
    update_profesor,
    delete_profesor,
)


class ProfesoresPantalla(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Datos en memoria (siempre vienen de SQLite)
        self.profesores = []

        titulo = ctk.CTkLabel(
            self,
            text="Profesores",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        titulo.pack(anchor="w", padx=18, pady=(18, 6))

        descripcion = ctk.CTkLabel(
            self,
            text="Gestión de profesores (SQLite): alta, edición y borrado.",
            justify="left",
        )
        descripcion.pack(anchor="w", padx=18, pady=(0, 14))

        # Barra de acciones
        acciones = ctk.CTkFrame(self, corner_radius=12)
        acciones.pack(fill="x", padx=18, pady=(0, 12))

        btn_recargar = ctk.CTkButton(acciones, text="Recargar", command=self._recargar)
        btn_recargar.pack(side="left", padx=12, pady=12)

        btn_nuevo = ctk.CTkButton(acciones, text="Nuevo profesor", command=self._nuevo_profesor)
        btn_nuevo.pack(side="left", padx=12, pady=12)

        # Listado con scroll
        self.scroll = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.scroll.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self._recargar()

    def _recargar(self):
        # Cargamos desde SQLite y repintamos
        try:
            self.profesores = get_profesores()
            self._pintar_listado(self.profesores)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar profesores:\n{e}")

    def _pintar_listado(self, profesores):
        # Limpiamos el contenido anterior
        for widget in self.scroll.winfo_children():
            widget.destroy()

        if not profesores:
            empty = ctk.CTkLabel(self.scroll, text="No hay profesores para mostrar.")
            empty.pack(anchor="w", padx=12, pady=12)
            return

        for prof in profesores:
            self._crear_tarjeta_profesor(prof)

    def _crear_tarjeta_profesor(self, prof):
        tarjeta = ctk.CTkFrame(self.scroll, corner_radius=12)
        tarjeta.pack(fill="x", padx=12, pady=8)

        nombre_completo = f"{prof['nombre']} {prof['apellidos']}"
        email = prof["email"] if prof["email"] else "—"
        depto = prof["departamento"]

        info = ctk.CTkFrame(tarjeta, corner_radius=0)
        info.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        lbl_nombre = ctk.CTkLabel(info, text=nombre_completo, font=ctk.CTkFont(size=16, weight="bold"))
        lbl_nombre.pack(anchor="w")

        lbl_depto = ctk.CTkLabel(info, text=f"Departamento: {depto}")
        lbl_depto.pack(anchor="w", pady=(4, 0))

        lbl_email = ctk.CTkLabel(info, text=f"Email: {email}")
        lbl_email.pack(anchor="w", pady=(2, 0))

        acciones = ctk.CTkFrame(tarjeta, corner_radius=0)
        acciones.pack(side="right", padx=12, pady=12)

        ctk.CTkButton(acciones, text="Ver", width=90, command=lambda p=prof: self._ver_profesor(p)).pack(pady=(0, 8))
        ctk.CTkButton(acciones, text="Editar", width=90, command=lambda p=prof: self._editar_profesor(p)).pack(pady=(0, 8))
        ctk.CTkButton(acciones, text="Borrar", width=90, command=lambda p=prof: self._borrar_profesor(p)).pack()

    def _ver_profesor(self, prof):
        # Mostramos datos en un mensaje simple
        msg = (
            f"ID: {prof['id']}\n"
            f"Nombre: {prof['nombre']}\n"
            f"Apellidos: {prof['apellidos']}\n"
            f"Departamento: {prof['departamento']}\n"
            f"Email: {prof['email'] or '—'}"
        )
        messagebox.showinfo("Profesor", msg)

    def _nuevo_profesor(self):
        # Abrimos formulario vacío
        self._abrir_formulario(
            title="Nuevo profesor",
            initial=None
        )

    def _editar_profesor(self, prof):
        # Abrimos formulario precargado
        self._abrir_formulario(
            title="Editar profesor",
            initial=prof
        )

    def _borrar_profesor(self, prof):
        # Confirmación antes de borrar
        if not messagebox.askyesno("Confirmar borrado", f"¿Borrar a {prof['nombre']} {prof['apellidos']}?"):
            return

        try:
            delete_profesor(int(prof["id"]))
            self._recargar()
        except Exception as e:
            messagebox.showerror("No se puede borrar", f"Error al borrar:\n{e}")

    def _abrir_formulario(self, title: str, initial: dict | None):
        # Ventana modal para alta/edición
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("520x360")
        win.transient(self.winfo_toplevel())  # asociada a la ventana principal
        win.grab_set()  # modal (bloquea la ventana principal hasta cerrar)

        header = ctk.CTkLabel(win, text=title, font=ctk.CTkFont(size=18, weight="bold"))
        header.pack(anchor="w", padx=18, pady=(18, 10))

        form = ctk.CTkFrame(win, corner_radius=12)
        form.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        # Campos del formulario
        ctk.CTkLabel(form, text="Nombre").pack(anchor="w", padx=12, pady=(12, 0))
        ent_nombre = ctk.CTkEntry(form)
        ent_nombre.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Apellidos").pack(anchor="w", padx=12, pady=(6, 0))
        ent_apellidos = ctk.CTkEntry(form)
        ent_apellidos.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Departamento").pack(anchor="w", padx=12, pady=(6, 0))
        ent_departamento = ctk.CTkEntry(form)
        ent_departamento.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Email (opcional)").pack(anchor="w", padx=12, pady=(6, 0))
        ent_email = ctk.CTkEntry(form)
        ent_email.pack(fill="x", padx=12, pady=(6, 12))

        # Si es edición, precargamos
        profesor_id = None
        if initial:
            profesor_id = int(initial["id"])
            ent_nombre.insert(0, initial["nombre"])
            ent_apellidos.insert(0, initial["apellidos"])
            ent_departamento.insert(0, initial["departamento"])
            if initial.get("email"):
                ent_email.insert(0, initial["email"])

        # Barra inferior de botones
        bottom = ctk.CTkFrame(win, corner_radius=0)
        bottom.pack(fill="x", padx=18, pady=(0, 18))

        def guardar():
            # Validación mínima (lo serio lo valida SQLite también)
            nombre = ent_nombre.get().strip()
            apellidos = ent_apellidos.get().strip()
            departamento = ent_departamento.get().strip()
            email = ent_email.get().strip() or None

            if not nombre or not apellidos or not departamento:
                messagebox.showwarning("Faltan datos", "Nombre, apellidos y departamento son obligatorios.")
                return

            try:
                if profesor_id is None:
                    insert_profesor(nombre, apellidos, departamento, email)
                else:
                    update_profesor(profesor_id, nombre, apellidos, departamento, email)

                win.destroy()
                self._recargar()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

        ctk.CTkButton(bottom, text="Cancelar", command=win.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(bottom, text="Guardar", command=guardar).pack(side="right")