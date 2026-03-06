import customtkinter as ctk
from tkinter import messagebox

from db.db import (
    get_asignaturas,
    insert_asignatura,
    update_asignatura,
    delete_asignatura,
)


class AsignaturasPantalla(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.asignaturas = []

        titulo = ctk.CTkLabel(
            self,
            text="Asignaturas",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        titulo.pack(anchor="w", padx=18, pady=(18, 6))

        descripcion = ctk.CTkLabel(
            self,
            text="Gestión de asignaturas: alta, edición y borrado.",
            justify="left",
        )
        descripcion.pack(anchor="w", padx=18, pady=(0, 14))

        acciones = ctk.CTkFrame(self, corner_radius=12)
        acciones.pack(fill="x", padx=18, pady=(0, 12))

        ctk.CTkButton(acciones, text="Recargar", command=self._recargar).pack(side="left", padx=12, pady=12)
        ctk.CTkButton(acciones, text="Nueva asignatura", command=self._nuevo).pack(side="left", padx=12, pady=12)

        self.scroll = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.scroll.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self._recargar()

    def _recargar(self):
        try:
            self.asignaturas = get_asignaturas()
            self._pintar_listado(self.asignaturas)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar asignaturas:\n{e}")

    def _pintar_listado(self, asignaturas):
        for w in self.scroll.winfo_children():
            w.destroy()

        if not asignaturas:
            ctk.CTkLabel(self.scroll, text="No hay asignaturas para mostrar.").pack(anchor="w", padx=12, pady=12)
            return

        for asignatura in asignaturas:
            self._crear_tarjeta(asignatura)

    def _crear_tarjeta(self, asignatura):
        tarjeta = ctk.CTkFrame(self.scroll, corner_radius=12)
        tarjeta.pack(fill="x", padx=12, pady=8)

        info = ctk.CTkFrame(tarjeta, corner_radius=0)
        info.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(
            info,
            text=asignatura["nombre"],
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Departamento: {asignatura['departamento']}",
        ).pack(anchor="w", pady=(4, 0))

        acciones = ctk.CTkFrame(tarjeta, corner_radius=0)
        acciones.pack(side="right", padx=12, pady=12)

        ctk.CTkButton(
            acciones,
            text="Editar",
            width=90,
            command=lambda x=asignatura: self._editar(x)
        ).pack(pady=(0, 8))

        ctk.CTkButton(
            acciones,
            text="Borrar",
            width=90,
            command=lambda x=asignatura: self._borrar(x)
        ).pack()

    def _nuevo(self):
        self._formulario("Nueva asignatura", None)

    def _editar(self, asignatura):
        self._formulario("Editar asignatura", asignatura)

    def _borrar(self, asignatura):
        if not messagebox.askyesno("Confirmar", f"¿Borrar asignatura '{asignatura['nombre']}'?"):
            return

        try:
            delete_asignatura(int(asignatura["id"]))
            self._recargar()
        except Exception as e:
            messagebox.showwarning("No se puede borrar", str(e))

    def _formulario(self, title: str, initial: dict | None):
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("560x320")
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

        ctk.CTkLabel(form, text="Nombre").pack(anchor="w", padx=12, pady=(12, 0))
        ent_nombre = ctk.CTkEntry(form)
        ent_nombre.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Departamento").pack(anchor="w", padx=12, pady=(6, 0))
        ent_departamento = ctk.CTkEntry(form)
        ent_departamento.pack(fill="x", padx=12, pady=(6, 12))

        asignatura_id = None
        if initial:
            asignatura_id = int(initial["id"])
            ent_nombre.insert(0, initial["nombre"])
            ent_departamento.insert(0, initial["departamento"])

        bottom = ctk.CTkFrame(win, corner_radius=0)
        bottom.pack(fill="x", padx=18, pady=(0, 18))

        def guardar():
            nombre = ent_nombre.get().strip()
            departamento = ent_departamento.get().strip()

            if not nombre or not departamento:
                messagebox.showwarning("Faltan datos", "Nombre y departamento son obligatorios.")
                return

            try:
                if asignatura_id is None:
                    insert_asignatura(nombre, departamento)
                else:
                    update_asignatura(asignatura_id, nombre, departamento)

                win.destroy()
                self._recargar()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

        ctk.CTkButton(bottom, text="Cancelar", command=win.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(bottom, text="Guardar", command=guardar).pack(side="right")

        ent_nombre.focus_set()