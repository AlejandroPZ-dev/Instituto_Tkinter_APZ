import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "instituto.db"
CSV_PATH = BASE_DIR / "database" / "materiales.csv"


def main():
    # Comprobamos que existen los archivos necesarios
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"No existe la base de datos: {DB_PATH}. "
            f"Ejecuta antes init_db.py para crear tablas y cargar seed."
        )

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"No existe el CSV: {CSV_PATH}")

    conn = sqlite3.connect(DB_PATH)
    try:
        # En SQLite, las claves foráneas se activan por conexión
        conn.execute("PRAGMA foreign_keys = ON;")

        # Dejamos la tabla material limpia antes de cargar el CSV (evita duplicados)
        conn.execute("DELETE FROM material;")
        conn.commit()

        sql = """
            INSERT INTO material (aula_id, nombre, descripcion)
            VALUES (?, ?, ?);
        """

        inserted = 0
        errors = 0

        with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)

            # Validamos que el CSV tenga las columnas esperadas
            required = {"aula_id", "nombre", "descripcion"}
            if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
                raise ValueError(
                    f"El CSV debe tener cabeceras: {sorted(required)}. "
                    f"Encontradas: {reader.fieldnames}"
                )

            for line_num, row in enumerate(reader, start=2):  # 2 porque la cabecera es la línea 1
                aula_id_raw = (row.get("aula_id") or "").strip()
                nombre = (row.get("nombre") or "").strip()
                descripcion = (row.get("descripcion") or "").strip()

                # Validaciones mínimas para no chocar con el schema
                if not aula_id_raw.isdigit():
                    print(f"Línea {line_num}: aula_id inválido -> {aula_id_raw!r}")
                    errors += 1
                    continue

                if not nombre:
                    print(f"Línea {line_num}: nombre vacío (no permitido)")
                    errors += 1
                    continue

                # Si descripción está vacía, insertamos NULL
                descripcion_val = descripcion if descripcion else None

                try:
                    conn.execute(sql, (int(aula_id_raw), nombre, descripcion_val))
                    inserted += 1
                except Exception as e:
                    print(f"Línea {line_num}: error insertando -> {e}")
                    errors += 1

        conn.commit()
        print(f"Carga terminada. Insertados: {inserted}. Errores: {errors}.")
        print(f"   CSV: {CSV_PATH}")
        print(f"   DB : {DB_PATH}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()