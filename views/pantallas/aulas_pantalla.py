import customtkinter as ctk
from tkinter import messagebox
from db.db import get_aulas, insert_aula, update_aula, delete_aula


class AulasPantalla(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.aulas = []

        titulo = ctk.CTkLabel(
            self,
            text="Aulas",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(anchor="w", padx=18, pady=(18, 6))

        descripcion = ctk.CTkLabel(
            self,
            text="Gestión de aulas: alta, edición y borrado.",
            justify="left",
        )
        descripcion.pack(anchor="w", padx=18, pady=(0, 14))

        acciones = ctk.CTkFrame(self, corner_radius=12)
        acciones.pack(fill="x", padx=18, pady=(0, 12))

        ctk.CTkButton(acciones, text="Recargar", command=self._recargar).pack(side="left", padx=12, pady=12)
        ctk.CTkButton(acciones, text="Nueva aula", command=self._nuevo).pack(side="left", padx=12, pady=12)

        self.scroll = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.scroll.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self._recargar()

    def _recargar(self):
        try:
            self.aulas = get_aulas()
            self._pintar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar aulas:\n{e}")

    def _pintar(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        if not self.aulas:
            ctk.CTkLabel(self.scroll, text="No hay aulas para mostrar.").pack(anchor="w", padx=12, pady=12)
            return

        for aula in self.aulas:
            self._crear_tarjeta_aula(aula)

    def _crear_tarjeta_aula(self, aula):
        card = ctk.CTkFrame(self.scroll, corner_radius=12)
        card.pack(fill="x", padx=12, pady=8)

        info = ctk.CTkFrame(card, corner_radius=0)
        info.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(
            info,
            text=f"Aula {aula['codigo']}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Capacidad: {aula['capacidad']}"
        ).pack(anchor="w", pady=(4, 0))

        actions = ctk.CTkFrame(card, corner_radius=0)
        actions.pack(side="right", padx=12, pady=12)

        ctk.CTkButton(actions, text="Editar", width=90, command=lambda x=aula: self._editar(x)).pack(pady=(0, 8))
        ctk.CTkButton(actions, text="Borrar", width=90, command=lambda x=aula: self._borrar(x)).pack()

    def _nuevo(self):
        self._form("Nueva aula", None)

    def _editar(self, aula):
        self._form("Editar aula", aula)

    def _borrar(self, aula):
        if not messagebox.askyesno("Confirmar", f"¿Borrar aula {aula['codigo']}?"):
            return

        try:
            delete_aula(int(aula["id"]))
            self._recargar()
        except Exception as e:
            messagebox.showwarning("No se puede borrar", str(e))

    def _form(self, title, initial):
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("520x300")
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

        ctk.CTkLabel(form, text="Código").pack(anchor="w", padx=12, pady=(12, 0))
        ent_codigo = ctk.CTkEntry(form)
        ent_codigo.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Capacidad").pack(anchor="w", padx=12, pady=(6, 0))
        ent_cap = ctk.CTkEntry(form)
        ent_cap.pack(fill="x", padx=12, pady=(6, 12))

        aula_id = None
        if initial:
            aula_id = int(initial["id"])
            ent_codigo.insert(0, str(initial["codigo"]))
            ent_cap.insert(0, str(initial["capacidad"]))

        bottom = ctk.CTkFrame(win, corner_radius=0)
        bottom.pack(fill="x", padx=18, pady=(0, 18))

        def guardar():
            codigo = ent_codigo.get().strip()
            cap_raw = ent_cap.get().strip()

            if not codigo:
                messagebox.showwarning("Faltan datos", "El código es obligatorio.")
                return

            if not cap_raw.isdigit():
                messagebox.showwarning("Dato inválido", "Capacidad debe ser un número entero.")
                return

            capacidad = int(cap_raw)

            if capacidad <= 0:
                messagebox.showwarning("Dato inválido", "Capacidad debe ser mayor que 0.")
                return

            try:
                if aula_id is None:
                    insert_aula(codigo, capacidad)
                else:
                    update_aula(aula_id, codigo, capacidad)

                win.destroy()
                self._recargar()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

        ctk.CTkButton(bottom, text="Cancelar", command=win.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(bottom, text="Guardar", command=guardar).pack(side="right")

        ent_codigo.focus_set()