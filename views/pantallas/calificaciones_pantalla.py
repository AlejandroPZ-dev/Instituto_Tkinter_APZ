import csv
from pathlib import Path

import customtkinter as ctk
from tkinter import messagebox, filedialog

from db.db import (
    get_calificaciones,
    get_calificaciones_por_alumno_y_anio,
    get_alumnos,
    get_alumnos_ids_ordenados,
    get_alumno_by_id,
    get_clases,
    get_convocatorias,
    insert_calificacion,
    update_calificacion,
    delete_calificacion,
)


class CalificacionesPantalla(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.calificaciones = []
        self.alumnos_ids = []
        self.alumno_actual_id = None

        self._build_ui()
        self._cargar_alumnos_navegacion()
        self._recargar()

    def _build_ui(self):
        titulo = ctk.CTkLabel(
            self,
            text="Calificaciones",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        titulo.pack(anchor="w", padx=18, pady=(18, 6))

        descripcion = ctk.CTkLabel(
            self,
            text="Gestión de calificaciones: alta, edición, borrado, filtro y exportación CSV.",
            justify="left",
        )
        descripcion.pack(anchor="w", padx=18, pady=(0, 14))

        acciones = ctk.CTkFrame(self, corner_radius=12)
        acciones.pack(fill="x", padx=18, pady=(0, 12))

        ctk.CTkButton(acciones, text="Recargar", command=self._recargar).pack(side="left", padx=8, pady=12)
        ctk.CTkButton(acciones, text="Nueva calificación", command=self._nuevo).pack(side="left", padx=8, pady=12)
        ctk.CTkButton(acciones, text="Exportar CSV", command=self._exportar_csv).pack(side="left", padx=8, pady=12)

        nav = ctk.CTkFrame(self, corner_radius=12)
        nav.pack(fill="x", padx=18, pady=(0, 12))

        ctk.CTkLabel(nav, text="Alumno").pack(side="left", padx=(12, 6), pady=12)

        self.alumno_var = ctk.StringVar(value="")
        self.cmb_alumno = ctk.CTkOptionMenu(nav, variable=self.alumno_var, values=["Todos"], command=lambda _v: self._aplicar_filtro())
        self.cmb_alumno.pack(side="left", padx=6, pady=12)

        ctk.CTkButton(nav, text="Anterior", width=100, command=self._alumno_anterior).pack(side="left", padx=6, pady=12)
        ctk.CTkButton(nav, text="Siguiente", width=100, command=self._alumno_siguiente).pack(side="left", padx=6, pady=12)

        ctk.CTkLabel(nav, text="Año académico").pack(side="left", padx=(18, 6), pady=12)

        self.anio_entry = ctk.CTkEntry(nav, width=140, placeholder_text="Ej: 2025-2026")
        self.anio_entry.pack(side="left", padx=6, pady=12)

        ctk.CTkButton(nav, text="Filtrar", command=self._aplicar_filtro).pack(side="left", padx=6, pady=12)
        ctk.CTkButton(nav, text="Quitar filtro", command=self._quitar_filtro).pack(side="left", padx=6, pady=12)

        self.info_alumno_label = ctk.CTkLabel(self, text="")
        self.info_alumno_label.pack(anchor="w", padx=18, pady=(0, 8))

        self.scroll = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.scroll.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _cargar_alumnos_navegacion(self):
        try:
            alumnos = get_alumnos()
            self.alumnos_ids = get_alumnos_ids_ordenados()

            labels = ["Todos"]
            self.alumnos_map = {"Todos": None}

            for a in alumnos:
                label = f"{a['apellidos']}, {a['nombre']}"
                self.alumnos_map[label] = a["id"]
                labels.append(label)

            self.cmb_alumno.configure(values=labels)
            self.alumno_var.set("Todos")

            if self.alumnos_ids:
                self.alumno_actual_id = self.alumnos_ids[0]

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar alumnos:\n{e}")

    def _recargar(self):
        try:
            self.calificaciones = get_calificaciones()
            self._pintar_listado(self.calificaciones)
            self._actualizar_info_alumno()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar calificaciones:\n{e}")

    def _pintar_listado(self, calificaciones):
        for w in self.scroll.winfo_children():
            w.destroy()

        if not calificaciones:
            ctk.CTkLabel(self.scroll, text="No hay calificaciones para mostrar.").pack(anchor="w", padx=12, pady=12)
            return

        for cal in calificaciones:
            self._crear_tarjeta(cal)

    def _crear_tarjeta(self, cal):
        tarjeta = ctk.CTkFrame(self.scroll, corner_radius=12)
        tarjeta.pack(fill="x", padx=12, pady=8)

        info = ctk.CTkFrame(tarjeta, corner_radius=0)
        info.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(
            info,
            text=f"{cal['alumno']} - {cal['asignatura']}",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(info, text=f"Convocatoria: {cal['convocatoria']}").pack(anchor="w", pady=(4, 0))
        ctk.CTkLabel(info, text=f"Año académico: {cal['anio_academico']}").pack(anchor="w", pady=(2, 0))
        ctk.CTkLabel(info, text=f"Nota: {cal['nota']}").pack(anchor="w", pady=(2, 0))

        acciones = ctk.CTkFrame(tarjeta, corner_radius=0)
        acciones.pack(side="right", padx=12, pady=12)

        ctk.CTkButton(acciones, text="Editar", width=90, command=lambda x=cal: self._editar(x)).pack(pady=(0, 8))
        ctk.CTkButton(acciones, text="Borrar", width=90, command=lambda x=cal: self._borrar(x)).pack()

    def _nuevo(self):
        self._formulario("Nueva calificación", None)

    def _editar(self, cal):
        self._formulario("Editar calificación", cal)

    def _borrar(self, cal):
        if not messagebox.askyesno("Confirmar", f"¿Borrar calificación de '{cal['alumno']}' en '{cal['asignatura']}'?"):
            return

        try:
            delete_calificacion(int(cal["id"]))
            self._aplicar_filtro()
        except Exception as e:
            messagebox.showwarning("No se puede borrar", str(e))

    def _formulario(self, title: str, initial: dict | None):
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("640x460")
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
            alumnos = get_alumnos()
            clases = get_clases()
            convocatorias = get_convocatorias()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar datos auxiliares:\n{e}")
            win.destroy()
            return

        if not alumnos:
            messagebox.showwarning("Sin alumnos", "No hay alumnos en la base de datos.")
            win.destroy()
            return

        if not clases:
            messagebox.showwarning("Sin clases", "No hay clases en la base de datos.")
            win.destroy()
            return

        if not convocatorias:
            messagebox.showwarning("Sin convocatorias", "No hay convocatorias en la base de datos.")
            win.destroy()
            return

        alumnos_map = {
            f"{a['apellidos']}, {a['nombre']}": a["id"]
            for a in alumnos
        }

        clases_map = {
            f"{c['asignatura']} | {c['aula']} | {c['anio_academico']}": c["id"]
            for c in clases
        }

        convocatorias_map = {
            c["nombre"]: c["id"]
            for c in convocatorias
        }

        alumnos_values = list(alumnos_map.keys())
        clases_values = list(clases_map.keys())
        convocatorias_values = list(convocatorias_map.keys())

        ctk.CTkLabel(form, text="Alumno").pack(anchor="w", padx=12, pady=(12, 0))
        alumno_var = ctk.StringVar(value=alumnos_values[0])
        cmb_alumno = ctk.CTkOptionMenu(form, variable=alumno_var, values=alumnos_values)
        cmb_alumno.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Clase").pack(anchor="w", padx=12, pady=(6, 0))
        clase_var = ctk.StringVar(value=clases_values[0])
        cmb_clase = ctk.CTkOptionMenu(form, variable=clase_var, values=clases_values)
        cmb_clase.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Convocatoria").pack(anchor="w", padx=12, pady=(6, 0))
        convocatoria_var = ctk.StringVar(value=convocatorias_values[0])
        cmb_convocatoria = ctk.CTkOptionMenu(form, variable=convocatoria_var, values=convocatorias_values)
        cmb_convocatoria.pack(fill="x", padx=12, pady=(6, 8))

        ctk.CTkLabel(form, text="Nota").pack(anchor="w", padx=12, pady=(6, 0))
        ent_nota = ctk.CTkEntry(form, placeholder_text="Valor entre 0 y 10")
        ent_nota.pack(fill="x", padx=12, pady=(6, 12))

        calificacion_id = None
        if initial:
            calificacion_id = int(initial["id"])

            alumno_inicial = next(
                (label for label, aid in alumnos_map.items() if aid == initial["alumno_id"]),
                alumnos_values[0]
            )
            clase_inicial = next(
                (label for label, cid in clases_map.items() if cid == initial["clase_id"]),
                clases_values[0]
            )
            convocatoria_inicial = next(
                (label for label, cid in convocatorias_map.items() if cid == initial["convocatoria_id"]),
                convocatorias_values[0]
            )

            alumno_var.set(alumno_inicial)
            clase_var.set(clase_inicial)
            convocatoria_var.set(convocatoria_inicial)
            ent_nota.insert(0, str(initial["nota"]))

        bottom = ctk.CTkFrame(win, corner_radius=0)
        bottom.pack(fill="x", padx=18, pady=(0, 18))

        def guardar():
            alumno_id = alumnos_map[alumno_var.get()]
            clase_id = clases_map[clase_var.get()]
            convocatoria_id = convocatorias_map[convocatoria_var.get()]
            nota_raw = ent_nota.get().strip().replace(",", ".")

            try:
                nota = float(nota_raw)
            except ValueError:
                messagebox.showwarning("Dato inválido", "La nota debe ser numérica.")
                return

            if nota < 0 or nota > 10:
                messagebox.showwarning("Dato inválido", "La nota debe estar entre 0 y 10.")
                return

            try:
                if calificacion_id is None:
                    insert_calificacion(alumno_id, clase_id, convocatoria_id, nota)
                else:
                    update_calificacion(calificacion_id, alumno_id, clase_id, convocatoria_id, nota)

                win.destroy()
                self._aplicar_filtro()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

        ctk.CTkButton(bottom, text="Cancelar", command=win.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(bottom, text="Guardar", command=guardar).pack(side="right")

        ent_nota.focus_set()

    def _aplicar_filtro(self):
        alumno_label = self.alumno_var.get()
        anio = self.anio_entry.get().strip()

        alumno_id = self.alumnos_map.get(alumno_label)

        try:
            if alumno_id is not None and anio:
                self.alumno_actual_id = alumno_id
                filtradas = get_calificaciones_por_alumno_y_anio(alumno_id, anio)
            else:
                filtradas = get_calificaciones()

            self.calificaciones = filtradas
            self._pintar_listado(self.calificaciones)
            self._actualizar_info_alumno()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aplicar filtro:\n{e}")

    def _quitar_filtro(self):
        self.alumno_var.set("Todos")
        self.anio_entry.delete(0, "end")
        self._recargar()

    def _alumno_anterior(self):
        if not self.alumnos_ids or self.alumno_actual_id is None:
            return

        try:
            idx = self.alumnos_ids.index(self.alumno_actual_id)
        except ValueError:
            idx = 0

        if idx > 0:
            self.alumno_actual_id = self.alumnos_ids[idx - 1]
            self._seleccionar_alumno_actual()

    def _alumno_siguiente(self):
        if not self.alumnos_ids or self.alumno_actual_id is None:
            return

        try:
            idx = self.alumnos_ids.index(self.alumno_actual_id)
        except ValueError:
            idx = 0

        if idx < len(self.alumnos_ids) - 1:
            self.alumno_actual_id = self.alumnos_ids[idx + 1]
            self._seleccionar_alumno_actual()

    def _seleccionar_alumno_actual(self):
        alumno = get_alumno_by_id(self.alumno_actual_id)
        if not alumno:
            return

        label = f"{alumno['apellidos']}, {alumno['nombre']}"
        self.alumno_var.set(label)
        self._aplicar_filtro()

    def _actualizar_info_alumno(self):
        if self.alumno_actual_id is None:
            self.info_alumno_label.configure(text="")
            return

        alumno = get_alumno_by_id(self.alumno_actual_id)
        if not alumno:
            self.info_alumno_label.configure(text="")
            return

        texto = f"Alumno actual: {alumno['nombre']} {alumno['apellidos']}"
        self.info_alumno_label.configure(text=texto)

    def _exportar_csv(self):
        if not self.calificaciones:
            messagebox.showwarning("Sin datos", "No hay calificaciones para exportar.")
            return

        default_name = "calificaciones.csv"
        file_path = filedialog.asksaveasfilename(
            title="Guardar CSV",
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV files", "*.csv")],
        )

        if not file_path:
            return

        try:
            with open(Path(file_path), "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["Alumno", "Asignatura", "Convocatoria", "Año académico", "Nota"])

                for cal in self.calificaciones:
                    writer.writerow([
                        cal["alumno"],
                        cal["asignatura"],
                        cal["convocatoria"],
                        cal["anio_academico"],
                        cal["nota"],
                    ])

            messagebox.showinfo("Exportación completada", f"CSV guardado en:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el CSV:\n{e}")