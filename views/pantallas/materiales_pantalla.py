import customtkinter as ctk
from tkinter import messagebox, filedialog

from db.db import (
    get_materiales,
    get_aulas_ids,
    insert_material,
    update_material,
    delete_material,
    import_materiales_desde_csv,
)


class MaterialesPantalla(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.materiales = []

        titulo = ctk.CTkLabel(
            self,
            text="Materiales",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        titulo.pack(anchor="w", padx=18, pady=(18, 6))

        descripcion = ctk.CTkLabel(
            self,
            text="Gestión de materiales: alta, edición y borrado.",
            justify="left",
        )
        descripcion.pack(anchor="w", padx=18, pady=(0, 14))

        acciones = ctk.CTkFrame(self, corner_radius=12)
        acciones.pack(fill="x", padx=18, pady=(0, 12))

        ctk.CTkButton(acciones, text="Recargar", command=self._recargar).pack(side="left", padx=12, pady=12)
        ctk.CTkButton(acciones, text="Nuevo material", command=self._nuevo).pack(side="left", padx=12, pady=12)
        ctk.CTkButton(acciones, text="Importar CSV", command=self._importar_csv).pack(side="left", padx=12, pady=12)

        self.scroll = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.scroll.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self._recargar()

    def _recargar(self):
        try:
            self.materiales = get_materiales()
            self._pintar_listado(self.materiales)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar materiales:\n{e}")

    def _pintar_listado(self, materiales):
        for w in self.scroll.winfo_children():
            w.destroy()

        if not materiales:
            ctk.CTkLabel(self.scroll, text="No hay materiales para mostrar.").pack(anchor="w", padx=12, pady=12)
            return

        for material in materiales:
            self._crear_tarjeta(material)

    def _crear_tarjeta(self, material):
        tarjeta = ctk.CTkFrame(self.scroll, corner_radius=12)
        tarjeta.pack(fill="x", padx=12, pady=8)

        info = ctk.CTkFrame(tarjeta, corner_radius=0)
        info.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(
            info,
            text=material["nombre"],
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Aula: {material['aula_id']}"
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkLabel(
            info,
            text=f"Descripción: {material['descripcion'] or '—'}",
            justify="left"
        ).pack(anchor="w", pady=(2, 0))

        acciones = ctk.CTkFrame(tarjeta, corner_radius=0)
        acciones.pack(side="right", padx=12, pady=12)

        ctk.CTkButton(
            acciones,
            text="Editar",
            width=90,
            command=lambda x=material: self._editar(x)
        ).pack(pady=(0, 8))

        ctk.CTkButton(
            acciones,
            text="Borrar",
            width=90,
            command=lambda x=material: self._borrar(x)
        ).pack()

    def _nuevo(self):
        self._formulario("Nuevo material", None)

    def _editar(self, material):
        self._formulario("Editar material", material)

    def _borrar(self, material):
        if not messagebox.askyesno("Confirmar", f"¿Borrar material '{material['nombre']}'?"):
            return

        try:
            delete_material(int(material["id"]))
            self._recargar()
        except Exception as e:
            messagebox.showwarning("No se puede borrar", str(e))

    def _formulario(self, title: str, initial: dict | None):
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("560x380")
        win.transient(self.winfo_toplevel())
        win.grab_set()
        win.resizable(False, False)
        win.focus()

        ctk.CTkLabel(
            win,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=18, pady=(18, 10))

        form = ctk.CTkFrame(win, corner_radius=12)
        form.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        try:
            aulas = get_aulas_ids()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar aulas:\n{e}")
            win.destroy()
            return

        if not aulas:
            messagebox.showwarning("Sin aulas", "No hay aulas en la base de datos. Crea aulas primero.")
            win.destroy()
            return

        ctk.CTkLabel(form, text="Aula (aula_id)").pack(anchor="w", padx=12, pady=(12, 0))
        aula_var = ctk.StringVar(value=str(aulas[0]))
        cmb_aula = ctk.CTkOptionMenu(form, variable=aula_var, values=[str(x) for x in aulas])
        cmb_aula.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Nombre").pack(anchor="w", padx=12, pady=(6, 0))
        ent_nombre = ctk.CTkEntry(form)
        ent_nombre.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Descripción (opcional)").pack(anchor="w", padx=12, pady=(6, 0))
        ent_desc = ctk.CTkEntry(form)
        ent_desc.pack(fill="x", padx=12, pady=(6, 12))

        material_id = None
        if initial:
            material_id = int(initial["id"])
            aula_var.set(str(initial["aula_id"]))
            ent_nombre.insert(0, initial["nombre"])
            if initial.get("descripcion"):
                ent_desc.insert(0, initial["descripcion"])

        bottom = ctk.CTkFrame(win, corner_radius=0)
        bottom.pack(fill="x", padx=18, pady=(0, 18))

        def guardar():
            aula_id = int(aula_var.get())
            nombre = ent_nombre.get().strip()
            desc = ent_desc.get().strip() or None

            if not nombre:
                messagebox.showwarning("Faltan datos", "El nombre es obligatorio.")
                return

            try:
                if material_id is None:
                    insert_material(aula_id, nombre, desc)
                else:
                    update_material(material_id, aula_id, nombre, desc)

                win.destroy()
                self._recargar()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

        ctk.CTkButton(bottom, text="Cancelar", command=win.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(bottom, text="Guardar", command=guardar).pack(side="right")

        ent_nombre.focus_set()

    def _importar_csv(self):
        csv_path = filedialog.askopenfilename(
            title="Seleccionar CSV de materiales",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )

        if not csv_path:
            return

        reemplazar = messagebox.askyesno(
            "Importación de materiales",
            "¿Quieres borrar los materiales actuales antes de importar el CSV?"
        )

        try:
            insertados, errores = import_materiales_desde_csv(
                csv_path,
                limpiar_antes=reemplazar
            )

            self._recargar()

            messagebox.showinfo(
                "Importación completada",
                f"Insertados: {insertados}\nErrores: {errores}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo importar el CSV:\n{e}")