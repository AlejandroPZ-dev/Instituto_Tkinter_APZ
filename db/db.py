import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "instituto.db"


def get_connection():
    # Abrimos conexión a SQLite
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # En SQLite, las claves foráneas se activan por conexión
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def get_profesores_combo() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT profesor_id, nombre, apellidos
            FROM profesor
            ORDER BY apellidos, nombre
        """).fetchall()

    return [
        {
            "id": r["profesor_id"],
            "label": f'{r["apellidos"]}, {r["nombre"]}',
        }
        for r in rows
    ]


def get_profesores():
    # Devuelve lista de profesores como diccionarios
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT profesor_id, nombre, apellidos, departamento, email
            FROM profesor
            ORDER BY apellidos, nombre
        """).fetchall()

    return [
        {
            "id": r["profesor_id"],
            "nombre": r["nombre"],
            "apellidos": r["apellidos"],
            "departamento": r["departamento"],
            "email": r["email"],
        }
        for r in rows
    ]

def insert_profesor(nombre: str, apellidos: str, departamento: str, email: str | None):
    # Inserta un profesor y devuelve el id generado
    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO profesor (nombre, apellidos, departamento, email)
            VALUES (?, ?, ?, ?)
            """,
            (nombre, apellidos, departamento, email),
        )
        conn.commit()
        return cur.lastrowid


def update_profesor(profesor_id: int, nombre: str, apellidos: str, departamento: str, email: str | None):
    # Actualiza un profesor existente
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE profesor
            SET nombre = ?, apellidos = ?, departamento = ?, email = ?
            WHERE profesor_id = ?
            """,
            (nombre, apellidos, departamento, email, profesor_id),
        )
        conn.commit()


def delete_profesor(profesor_id: int):
    # Borra un profesor. Si está referenciado por otras tablas, SQLite lo impedirá.
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM profesor WHERE profesor_id = ?", (profesor_id,))
            conn.commit()
    except sqlite3.IntegrityError as e:
        # Error típico: FOREIGN KEY constraint failed
        raise ValueError("No se puede borrar: el profesor está asignado a clases u otros registros.") from e




def get_aulas_ids() -> list[int]:
    # Devuelve lista de aula_id disponibles (para elegir en formularios)
    with get_connection() as conn:
        rows = conn.execute("SELECT aula_id FROM aula ORDER BY aula_id").fetchall()
    return [int(r["aula_id"]) for r in rows]


def get_materiales() -> list[dict]:
    # Devuelve lista de materiales
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT material_id, aula_id, nombre, descripcion
            FROM material
            ORDER BY aula_id, nombre
        """).fetchall()

    return [
        {
            "id": r["material_id"],
            "aula_id": r["aula_id"],
            "nombre": r["nombre"],
            "descripcion": r["descripcion"],
        }
        for r in rows
    ]


def insert_material(aula_id: int, nombre: str, descripcion: str | None):
    # Inserta un material
    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO material (aula_id, nombre, descripcion)
            VALUES (?, ?, ?)
            """,
            (aula_id, nombre, descripcion),
        )
        conn.commit()
        return cur.lastrowid


def update_material(material_id: int, aula_id: int, nombre: str, descripcion: str | None):
    # Actualiza un material
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE material
            SET aula_id = ?, nombre = ?, descripcion = ?
            WHERE material_id = ?
            """,
            (aula_id, nombre, descripcion, material_id),
        )
        conn.commit()


def delete_material(material_id: int):
    # Borra un material
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM material WHERE material_id = ?", (material_id,))
            conn.commit()
    except sqlite3.IntegrityError as e:
        # Por si en el futuro material se relaciona con otras tablas
        raise ValueError("No se puede borrar: el material está referenciado por otros registros.") from e






# -------------------------
# AULAS (CRUD)
# -------------------------
def get_aulas_combo() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT aula_id, codigo
            FROM aula
            ORDER BY codigo
        """).fetchall()

    return [
        {
            "id": r["aula_id"],
            "label": r["codigo"],
        }
        for r in rows
    ]



def get_aulas() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT aula_id, codigo, capacidad
            FROM aula
            ORDER BY codigo
        """).fetchall()

    return [
        {
            "id": r["aula_id"],
            "codigo": r["codigo"],
            "capacidad": r["capacidad"],
        }
        for r in rows
    ]


def insert_aula(codigo: str, capacidad: int):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO aula (codigo, capacidad) VALUES (?, ?)",
            (codigo, capacidad),
        )
        conn.commit()
        return cur.lastrowid


def update_aula(aula_id: int, codigo: str, capacidad: int):
    with get_connection() as conn:
        conn.execute(
            "UPDATE aula SET codigo = ?, capacidad = ? WHERE aula_id = ?",
            (codigo, capacidad, aula_id),
        )
        conn.commit()


def delete_aula(aula_id: int):
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM aula WHERE aula_id = ?", (aula_id,))
            conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError("No se puede borrar el aula: está referenciada por materiales o clases.") from e


def get_aulas_ids() -> list[int]:
    with get_connection() as conn:
        rows = conn.execute("SELECT aula_id FROM aula ORDER BY aula_id").fetchall()
    return [int(r["aula_id"]) for r in rows]


# -------------------------
# ASIGNATURAS (CRUD)
# -------------------------
def get_asignaturas_combo() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT asignatura_id, nombre
            FROM asignatura
            ORDER BY nombre
        """).fetchall()

    return [
        {
            "id": r["asignatura_id"],
            "label": r["nombre"],
        }
        for r in rows
    ]



def get_asignaturas() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT asignatura_id, nombre, departamento
            FROM asignatura
            ORDER BY nombre
        """).fetchall()

    return [{"id": r["asignatura_id"], "nombre": r["nombre"], "departamento": r["departamento"]} for r in rows]


def insert_asignatura(nombre: str, departamento: str):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO asignatura (nombre, departamento) VALUES (?, ?)",
            (nombre, departamento),
        )
        conn.commit()
        return cur.lastrowid


def update_asignatura(asignatura_id: int, nombre: str, departamento: str):
    with get_connection() as conn:
        conn.execute(
            "UPDATE asignatura SET nombre = ?, departamento = ? WHERE asignatura_id = ?",
            (nombre, departamento, asignatura_id),
        )
        conn.commit()


def delete_asignatura(asignatura_id: int):
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM asignatura WHERE asignatura_id = ?", (asignatura_id,))
            conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError("No se puede borrar la asignatura: está referenciada por clases o calificaciones.") from e


def get_asignaturas_ids() -> list[int]:
    with get_connection() as conn:
        rows = conn.execute("SELECT asignatura_id FROM asignatura ORDER BY asignatura_id").fetchall()
    return [int(r["asignatura_id"]) for r in rows]


# -------------------------
# ALUMNOS (CRUD)  (ajusta columnas si tu schema cambia)
# -------------------------
def get_alumnos() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT alumno_id, nombre, apellidos, fecha_nacimiento, email
            FROM alumno
            ORDER BY apellidos, nombre
        """).fetchall()

    return [
        {
            "id": r["alumno_id"],
            "nombre": r["nombre"],
            "apellidos": r["apellidos"],
            "fecha_nacimiento": r["fecha_nacimiento"],
            "email": r["email"],
        }
        for r in rows
    ]


def insert_alumno(nombre: str, apellidos: str, fecha_nacimiento: str | None, email: str | None):
    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO alumno (nombre, apellidos, fecha_nacimiento, email)
            VALUES (?, ?, ?, ?)
            """,
            (nombre, apellidos, fecha_nacimiento, email),
        )
        conn.commit()
        return cur.lastrowid


def update_alumno(alumno_id: int, nombre: str, apellidos: str, fecha_nacimiento: str | None, email: str | None):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE alumno
            SET nombre = ?, apellidos = ?, fecha_nacimiento = ?, email = ?
            WHERE alumno_id = ?
            """,
            (nombre, apellidos, fecha_nacimiento, email, alumno_id),
        )
        conn.commit()


def delete_alumno(alumno_id: int):
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM alumno WHERE alumno_id = ?", (alumno_id,))
            conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError("No se puede borrar el alumno: tiene matrícula, clases o calificaciones asociadas.") from e


def get_alumnos_ids_ordenados() -> list[int]:
    with get_connection() as conn:
        rows = conn.execute("SELECT alumno_id FROM alumno ORDER BY apellidos, nombre").fetchall()
    return [int(r["alumno_id"]) for r in rows]


def get_alumno_by_id(alumno_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("""
            SELECT alumno_id, nombre, apellidos, fecha_nacimiento, email
            FROM alumno
            WHERE alumno_id = ?
        """, (alumno_id,)).fetchone()

    if row is None:
        return None

    return {
        "id": row["alumno_id"],
        "nombre": row["nombre"],
        "apellidos": row["apellidos"],
        "fecha_nacimiento": row["fecha_nacimiento"],
        "email": row["email"],
    }


# -------------------------
# PROFESORES (ya lo tienes, pero útil para combos en CLASES)
# -------------------------
def get_profesores_ids() -> list[int]:
    with get_connection() as conn:
        rows = conn.execute("SELECT profesor_id FROM profesor ORDER BY profesor_id").fetchall()
    return [int(r["profesor_id"]) for r in rows]


# -------------------------
# CLASES (CRUD)
# -------------------------
def get_clases() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                c.clase_id,
                c.profesor_id,
                c.asignatura_id,
                c.aula_id,
                c.anio_academico,
                p.nombre || ' ' || p.apellidos AS profesor,
                a.nombre AS asignatura,
                au.codigo AS aula
            FROM clase c
            JOIN profesor p ON p.profesor_id = c.profesor_id
            JOIN asignatura a ON a.asignatura_id = c.asignatura_id
            JOIN aula au ON au.aula_id = c.aula_id
            ORDER BY c.anio_academico DESC, a.nombre, p.apellidos, p.nombre
        """).fetchall()

    return [
        {
            "id": r["clase_id"],
            "profesor_id": r["profesor_id"],
            "asignatura_id": r["asignatura_id"],
            "aula_id": r["aula_id"],
            "anio_academico": r["anio_academico"],
            "profesor": r["profesor"],
            "asignatura": r["asignatura"],
            "aula": r["aula"],
        }
        for r in rows
    ]


def insert_clase(profesor_id: int, aula_id: int, asignatura_id: int, ano_academico: str):
    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO clase (profesor_id, aula_id, asignatura_id, anio_academico)
            VALUES (?, ?, ?, ?)
            """,
            (profesor_id, aula_id, asignatura_id, ano_academico),
        )
        conn.commit()
        return cur.lastrowid


def update_clase(clase_id: int, profesor_id: int, aula_id: int, asignatura_id: int, ano_academico: str):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE clase
            SET profesor_id = ?, aula_id = ?, asignatura_id = ?, anio_academico = ?
            WHERE clase_id = ?
            """,
            (profesor_id, aula_id, asignatura_id, ano_academico, clase_id),
        )
        conn.commit()


def delete_clase(clase_id: int):
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM clase WHERE clase_id = ?", (clase_id,))
            conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError("No se puede borrar la clase: tiene alumnos o calificaciones asociadas.") from e



# -------------------------
# CONVOCATORIAS
# -------------------------
def get_convocatorias() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT convocatoria_id, nombre
            FROM convocatoria
            ORDER BY convocatoria_id
        """).fetchall()

    return [
        {
            "id": r["convocatoria_id"],
            "nombre": r["nombre"],
        }
        for r in rows
    ]


def get_convocatorias_combo() -> list[dict]:
    rows = get_convocatorias()
    return [{"id": r["id"], "label": r["nombre"]} for r in rows]


# -------------------------
# CALIFICACIONES
# -------------------------
def get_calificaciones() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                cal.calificacion_id,
                cal.alumno_id,
                cal.clase_id,
                cal.convocatoria_id,
                cal.nota,
                al.nombre || ' ' || al.apellidos AS alumno,
                asi.nombre AS asignatura,
                conv.nombre AS convocatoria,
                c.anio_academico
            FROM calificacion cal
            JOIN alumno al ON al.alumno_id = cal.alumno_id
            JOIN clase c ON c.clase_id = cal.clase_id
            JOIN asignatura asi ON asi.asignatura_id = c.asignatura_id
            JOIN convocatoria conv ON conv.convocatoria_id = cal.convocatoria_id
            ORDER BY al.apellidos, al.nombre, c.anio_academico, asi.nombre, conv.convocatoria_id
        """).fetchall()

    return [
        {
            "id": r["calificacion_id"],
            "alumno_id": r["alumno_id"],
            "clase_id": r["clase_id"],
            "convocatoria_id": r["convocatoria_id"],
            "nota": r["nota"],
            "alumno": r["alumno"],
            "asignatura": r["asignatura"],
            "convocatoria": r["convocatoria"],
            "anio_academico": r["anio_academico"],
        }
        for r in rows
    ]
def insert_calificacion(alumno_id: int, clase_id: int, convocatoria_id: int, nota: float):
    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO calificacion (alumno_id, clase_id, convocatoria_id, nota)
            VALUES (?, ?, ?, ?)
            """,
            (alumno_id, clase_id, convocatoria_id, nota),
        )
        conn.commit()
        return cur.lastrowid

def update_calificacion(calificacion_id: int, alumno_id: int, clase_id: int, convocatoria_id: int, nota: float):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE calificacion
            SET alumno_id = ?, clase_id = ?, convocatoria_id = ?, nota = ?
            WHERE calificacion_id = ?
            """,
            (alumno_id, clase_id, convocatoria_id, nota, calificacion_id),
        )
        conn.commit()

def delete_calificacion(calificacion_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM calificacion WHERE calificacion_id = ?", (calificacion_id,))
        conn.commit()

def get_calificaciones_por_alumno_y_anio(alumno_id: int, anio_academico: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                cal.calificacion_id,
                cal.alumno_id,
                cal.clase_id,
                cal.convocatoria_id,
                cal.nota,
                al.nombre || ' ' || al.apellidos AS alumno,
                asi.nombre AS asignatura,
                conv.nombre AS convocatoria,
                c.anio_academico
            FROM calificacion cal
            JOIN alumno al ON al.alumno_id = cal.alumno_id
            JOIN clase c ON c.clase_id = cal.clase_id
            JOIN asignatura asi ON asi.asignatura_id = c.asignatura_id
            JOIN convocatoria conv ON conv.convocatoria_id = cal.convocatoria_id
            WHERE cal.alumno_id = ?
              AND c.anio_academico = ?
            ORDER BY asi.nombre, conv.convocatoria_id
        """, (alumno_id, anio_academico)).fetchall()

    return [
        {
            "id": r["calificacion_id"],
            "alumno_id": r["alumno_id"],
            "clase_id": r["clase_id"],
            "convocatoria_id": r["convocatoria_id"],
            "nota": r["nota"],
            "alumno": r["alumno"],
            "asignatura": r["asignatura"],
            "convocatoria": r["convocatoria"],
            "anio_academico": r["anio_academico"],
        }
        for r in rows
    ]





# -------------------------
# IMPORTACIÓN MATERIALES DESDE CSV (para el menú de la app)
# -------------------------
import csv

def import_materiales_desde_csv(csv_path: str, limpiar_antes: bool = False) -> tuple[int, int]:
    # Importa materiales desde un CSV con cabecera: aula_id,nombre,descripcion
    # Devuelve (insertados, errores)
    inserted = 0
    errors = 0

    with get_connection() as conn:
        if limpiar_antes:
            conn.execute("DELETE FROM material;")

        with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    aula_id = int((row.get("aula_id") or "").strip())
                    nombre = (row.get("nombre") or "").strip()
                    descripcion = (row.get("descripcion") or "").strip() or None

                    if not nombre:
                        errors += 1
                        continue

                    conn.execute(
                        "INSERT INTO material (aula_id, nombre, descripcion) VALUES (?, ?, ?)",
                        (aula_id, nombre, descripcion),
                    )
                    inserted += 1
                except Exception:
                    errors += 1

        conn.commit()

    return inserted, errors

def get_export_calificaciones(asignatura_id: int, convocatoria_id: int, anio_academico: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                al.nombre,
                al.apellidos,
                asi.nombre AS asignatura,
                conv.nombre AS convocatoria,
                c.anio_academico,
                cal.nota
            FROM calificacion cal
            JOIN alumno al ON al.alumno_id = cal.alumno_id
            JOIN clase c ON c.clase_id = cal.clase_id
            JOIN asignatura asi ON asi.asignatura_id = c.asignatura_id
            JOIN convocatoria conv ON conv.convocatoria_id = cal.convocatoria_id
            WHERE c.asignatura_id = ?
              AND cal.convocatoria_id = ?
              AND c.anio_academico = ?
            ORDER BY al.apellidos, al.nombre
        """, (asignatura_id, convocatoria_id, anio_academico)).fetchall()

    return [
        {
            "nombre": r["nombre"],
            "apellidos": r["apellidos"],
            "asignatura": r["asignatura"],
            "convocatoria": r["convocatoria"],
            "anio_academico": r["anio_academico"],
            "nota": r["nota"],
        }
        for r in rows
    ]