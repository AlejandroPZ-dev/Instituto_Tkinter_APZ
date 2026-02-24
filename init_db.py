import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "instituto.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"
SEED_PATH = BASE_DIR / "database" / "seed.sql"


def run_sql_file(conn: sqlite3.Connection, sql_path: Path):
    # Ejecuta el contenido de un archivo .sql completo
    sql = sql_path.read_text(encoding="utf-8")
    conn.executescript(sql)


def main():
    # Comprobaciones básicas
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"No existe {SCHEMA_PATH}")
    if not SEED_PATH.exists():
        raise FileNotFoundError(f"No existe {SEED_PATH}")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Conexión a SQLite (crea el archivo si no existe)
    conn = sqlite3.connect(DB_PATH)

    try:
        # Muy importante en SQLite: activar claves foráneas
        conn.execute("PRAGMA foreign_keys = ON;")

        # Ejecutamos schema y seed
        run_sql_file(conn, SCHEMA_PATH)
        run_sql_file(conn, SEED_PATH)

        conn.commit()
        print("Base de datos inicializada correctamente.")
        print(f"   DB: {DB_PATH}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
