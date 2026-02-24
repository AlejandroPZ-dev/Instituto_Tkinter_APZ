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
    # Borra un profesor (si hay RESTRICT en otras tablas, puede fallar)
    with get_connection() as conn:
        conn.execute("DELETE FROM profesor WHERE profesor_id = ?", (profesor_id,))
        conn.commit()