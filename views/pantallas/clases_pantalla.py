import customtkinter as ctk
from tkinter import messagebox

from db.db import (
    get_clases,
    get_profesores,
    get_asignaturas,
    get_aulas,
    insert_clase,
    update_clase,
    delete_clase,
)


class ClasesPantalla(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.clases = []

        titulo = ctk.CTkLabel(
            self,
            text="Clases",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        titulo.pack(anchor="w", padx=18, pady=(18, 6))

        descripcion = ctk.CTkLabel(
            self,
            text="Gestión de clases: profesor, asignatura, aula y año académico.",
            justify="left",
        )
        descripcion.pack(anchor="w", padx=18, pady=(0, 14))

        acciones = ctk.CTkFrame(self, corner_radius=12)
        acciones.pack(fill="x", padx=18, pady=(0, 12))

        ctk.CTkButton(acciones, text="Recargar", command=self._recargar).pack(side="left", padx=12, pady=12)
        ctk.CTkButton(acciones, text="Nueva clase", command=self._nuevo).pack(side="left", padx=12, pady=12)

        self.scroll = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.scroll.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self._recargar()

    def _recargar(self):
        try:
            self.clases = get_clases()
            self._pintar_listado(self.clases)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar clases:\n{e}")

    def _pintar_listado(self, clases):
        for w in self.scroll.winfo_children():
            w.destroy()

        if not clases:
            ctk.CTkLabel(self.scroll, text="No hay clases para mostrar.").pack(anchor="w", padx=12, pady=12)
            return

        for clase in clases:
            self._crear_tarjeta(clase)

    def _crear_tarjeta(self, clase):
        tarjeta = ctk.CTkFrame(self.scroll, corner_radius=12)
        tarjeta.pack(fill="x", padx=12, pady=8)

        info = ctk.CTkFrame(tarjeta, corner_radius=0)
        info.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        texto_profesor = clase.get("profesor", f"Profesor ID {clase['profesor_id']}")
        texto_asignatura = clase.get("asignatura", f"Asignatura ID {clase['asignatura_id']}")
        texto_aula = clase.get("aula", f"Aula ID {clase['aula_id']}")

        ctk.CTkLabel(
            info,
            text=texto_asignatura,
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Profesor: {texto_profesor}",
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkLabel(
            info,
            text=f"Aula: {texto_aula}",
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(
            info,
            text=f"Año académico: {clase['anio_academico']}",
        ).pack(anchor="w", pady=(2, 0))

        acciones = ctk.CTkFrame(tarjeta, corner_radius=0)
        acciones.pack(side="right", padx=12, pady=12)

        ctk.CTkButton(
            acciones,
            text="Editar",
            width=90,
            command=lambda x=clase: self._editar(x)
        ).pack(pady=(0, 8))

        ctk.CTkButton(
            acciones,
            text="Borrar",
            width=90,
            command=lambda x=clase: self._borrar(x)
        ).pack()

    def _nuevo(self):
        self._formulario("Nueva clase", None)

    def _editar(self, clase):
        self._formulario("Editar clase", clase)

    def _borrar(self, clase):
        nombre = clase.get("asignatura", f"ID {clase['id']}")
        if not messagebox.askyesno("Confirmar", f"¿Borrar la clase '{nombre}'?"):
            return

        try:
            delete_clase(int(clase["id"]))
            self._recargar()
        except Exception as e:
            messagebox.showwarning("No se puede borrar", str(e))

    def _formulario(self, title: str, initial: dict | None):
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("620x420")
        win.transient(self.winfo_toplevel())
        win.grab_set()
        win.resizable(False, False)
        win.focus()

        ctk.CTkLabel(
            win,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=18, pady=(18, 10))

        form = ctk.CTkFrame(win, corner_radius=12)
        form.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        try:
            profesores = get_profesores()
            asignaturas = get_asignaturas()
            aulas = get_aulas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar datos auxiliares:\n{e}")
            win.destroy()
            return

        if not profesores:
            messagebox.showwarning("Sin profesores", "No hay profesores en la base de datos.")
            win.destroy()
            return

        if not asignaturas:
            messagebox.showwarning("Sin asignaturas", "No hay asignaturas en la base de datos.")
            win.destroy()
            return

        if not aulas:
            messagebox.showwarning("Sin aulas", "No hay aulas en la base de datos.")
            win.destroy()
            return

        profesores_map = {
            f"{p['apellidos']}, {p['nombre']}": p["id"]
            for p in profesores
        }
        asignaturas_map = {
            a["nombre"]: a["id"]
            for a in asignaturas
        }
        aulas_map = {
            a["codigo"]: a["id"]
            for a in aulas
        }

        profesores_values = list(profesores_map.keys())
        asignaturas_values = list(asignaturas_map.keys())
        aulas_values = list(aulas_map.keys())

        ctk.CTkLabel(form, text="Profesor").pack(anchor="w", padx=12, pady=(12, 0))
        profesor_var = ctk.StringVar(value=profesores_values[0])
        cmb_profesor = ctk.CTkOptionMenu(form, variable=profesor_var, values=profesores_values)
        cmb_profesor.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Asignatura").pack(anchor="w", padx=12, pady=(6, 0))
        asignatura_var = ctk.StringVar(value=asignaturas_values[0])
        cmb_asignatura = ctk.CTkOptionMenu(form, variable=asignatura_var, values=asignaturas_values)
        cmb_asignatura.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Aula").pack(anchor="w", padx=12, pady=(6, 0))
        aula_var = ctk.StringVar(value=aulas_values[0])
        cmb_aula = ctk.CTkOptionMenu(form, variable=aula_var, values=aulas_values)
        cmb_aula.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Año académico").pack(anchor="w", padx=12, pady=(6, 0))
        ent_anio = ctk.CTkEntry(form, placeholder_text="Ej: 2025-2026")
        ent_anio.pack(fill="x", padx=12, pady=(6, 12))

        clase_id = None
        if initial:
            clase_id = int(initial["id"])

            profesor_inicial = next(
                (label for label, pid in profesores_map.items() if pid == initial["profesor_id"]),
                profesores_values[0]
            )
            asignatura_inicial = next(
                (label for label, aid in asignaturas_map.items() if aid == initial["asignatura_id"]),
                asignaturas_values[0]
            )
            aula_inicial = next(
                (label for label, auid in aulas_map.items() if auid == initial["aula_id"]),
                aulas_values[0]
            )

            profesor_var.set(profesor_inicial)
            asignatura_var.set(asignatura_inicial)
            aula_var.set(aula_inicial)
            ent_anio.insert(0, initial["anio_academico"])

        bottom = ctk.CTkFrame(win, corner_radius=0)
        bottom.pack(fill="x", padx=18, pady=(0, 18))

        def guardar():
            profesor_label = profesor_var.get()
            asignatura_label = asignatura_var.get()
            aula_label = aula_var.get()
            anio = ent_anio.get().strip()

            if not anio:
                messagebox.showwarning("Faltan datos", "El año académico es obligatorio.")
                return

            profesor_id = profesores_map[profesor_label]
            asignatura_id = asignaturas_map[asignatura_label]
            aula_id = aulas_map[aula_label]

            try:
                if clase_id is None:
                    insert_clase(profesor_id, aula_id, asignatura_id, anio)
                else:
                    update_clase(clase_id, profesor_id, aula_id, asignatura_id, anio)

                win.destroy()
                self._recargar()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

        ctk.CTkButton(bottom, text="Cancelar", command=win.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(bottom, text="Guardar", command=guardar).pack(side="right")

        ent_anio.focus_set()