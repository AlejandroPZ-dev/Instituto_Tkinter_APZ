import customtkinter as ctk
from tkinter import ttk, messagebox

from db.db import get_alumnos, insert_alumno, update_alumno, delete_alumno


class AlumnosPantalla(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.alumno_id_actual = None

        self._build_ui()
        self._load_data()

    def _build_ui(self):
        # Title
        titulo = ctk.CTkLabel(
            self,
            text="Alumnos",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        titulo.pack(anchor="w", padx=18, pady=(18, 10))

        # Main container
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        # Left: form
        form_frame = ctk.CTkFrame(main, width=320)
        form_frame.pack(side="left", fill="y", padx=(0, 12), pady=12)
        form_frame.pack_propagate(False)

        form_title = ctk.CTkLabel(
            form_frame,
            text="Formulario",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        form_title.pack(anchor="w", padx=16, pady=(16, 10))

        self.nombre_entry = ctk.CTkEntry(form_frame, placeholder_text="Nombre")
        self.nombre_entry.pack(fill="x", padx=16, pady=6)

        self.apellidos_entry = ctk.CTkEntry(form_frame, placeholder_text="Apellidos")
        self.apellidos_entry.pack(fill="x", padx=16, pady=6)

        self.fecha_entry = ctk.CTkEntry(form_frame, placeholder_text="Fecha nacimiento (YYYY-MM-DD)")
        self.fecha_entry.pack(fill="x", padx=16, pady=6)

        self.email_entry = ctk.CTkEntry(form_frame, placeholder_text="Email")
        self.email_entry.pack(fill="x", padx=16, pady=6)

        self.status_label = ctk.CTkLabel(form_frame, text="")
        self.status_label.pack(anchor="w", padx=16, pady=(10, 0))

        self.guardar_btn = ctk.CTkButton(form_frame, text="Guardar", command=self._guardar)
        self.guardar_btn.pack(fill="x", padx=16, pady=(16, 6))

        self.nuevo_btn = ctk.CTkButton(form_frame, text="Nuevo / Limpiar", command=self._limpiar_formulario)
        self.nuevo_btn.pack(fill="x", padx=16, pady=6)

        self.eliminar_btn = ctk.CTkButton(form_frame, text="Eliminar", command=self._eliminar)
        self.eliminar_btn.pack(fill="x", padx=16, pady=6)

        self.recargar_btn = ctk.CTkButton(form_frame, text="Recargar", command=self._load_data)
        self.recargar_btn.pack(fill="x", padx=16, pady=(6, 16))

        # Right: table
        table_frame = ctk.CTkFrame(main)
        table_frame.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=12)

        table_title = ctk.CTkLabel(
            table_frame,
            text="Listado de alumnos",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        table_title.pack(anchor="w", padx=16, pady=(16, 10))

        tree_container = ctk.CTkFrame(table_frame)
        tree_container.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        columns = ("id", "nombre", "apellidos", "fecha_nacimiento", "email")

        self.tree = ttk.Treeview(tree_container, columns=columns, show="headings", height=16)

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellidos", text="Apellidos")
        self.tree.heading("fecha_nacimiento", text="Fecha Nac.")
        self.tree.heading("email", text="Email")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nombre", width=140)
        self.tree.column("apellidos", width=180)
        self.tree.column("fecha_nacimiento", width=110, anchor="center")
        self.tree.column("email", width=220)

        scrollbar_y = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _load_data(self):
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load rows
        alumnos = get_alumnos()
        for alumno in alumnos:
            self.tree.insert(
                "",
                "end",
                values=(
                    alumno["id"],
                    alumno["nombre"],
                    alumno["apellidos"],
                    alumno["fecha_nacimiento"] or "",
                    alumno["email"] or "",
                ),
            )

        self._set_status(f"Registros cargados: {len(alumnos)}")

    def _on_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.alumno_id_actual = int(values[0])

        self.nombre_entry.delete(0, "end")
        self.nombre_entry.insert(0, values[1])

        self.apellidos_entry.delete(0, "end")
        self.apellidos_entry.insert(0, values[2])

        self.fecha_entry.delete(0, "end")
        self.fecha_entry.insert(0, values[3])

        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, values[4])

        self._set_status(f"Alumno seleccionado: ID {self.alumno_id_actual}")

    def _guardar(self):
        nombre = self.nombre_entry.get().strip()
        apellidos = self.apellidos_entry.get().strip()
        fecha_nacimiento = self.fecha_entry.get().strip() or None
        email = self.email_entry.get().strip() or None

        if not nombre or not apellidos:
            self._set_status("Nombre y apellidos son obligatorios.")
            return

        try:
            if self.alumno_id_actual is None:
                insert_alumno(nombre, apellidos, fecha_nacimiento, email)
                self._set_status("Alumno creado correctamente.")
            else:
                update_alumno(self.alumno_id_actual, nombre, apellidos, fecha_nacimiento, email)
                self._set_status("Alumno actualizado correctamente.")

            self._limpiar_formulario(recargar=False)
            self._load_data()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _eliminar(self):
        if self.alumno_id_actual is None:
            self._set_status("Selecciona un alumno para eliminar.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar borrado",
            "¿Seguro que quieres eliminar este alumno?"
        )
        if not confirmar:
            return

        try:
            delete_alumno(self.alumno_id_actual)
            self._set_status("Alumno eliminado correctamente.")
            self._limpiar_formulario(recargar=False)
            self._load_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _limpiar_formulario(self, recargar: bool = False):
        self.alumno_id_actual = None

        self.nombre_entry.delete(0, "end")
        self.apellidos_entry.delete(0, "end")
        self.fecha_entry.delete(0, "end")
        self.email_entry.delete(0, "end")

        self.tree.selection_remove(self.tree.selection())

        self._set_status("Formulario limpio. Modo nuevo registro.")

        if recargar:
            self._load_data()

    def _set_status(self, message: str):
        self.status_label.configure(text=message)