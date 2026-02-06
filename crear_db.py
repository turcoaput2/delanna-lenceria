import sqlite3

conn = sqlite3.connect("tienda.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    imagen TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Base de datos creada correctamente")
