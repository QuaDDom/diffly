# db/db.py
import sqlite3

def init_db():
    conn = sqlite3.connect("comparaciones.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comparaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            nombre_archivo_ref TEXT,
            nombre_archivo_act TEXT,
            resultado BLOB
        )
    """)
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect("comparaciones.db")
