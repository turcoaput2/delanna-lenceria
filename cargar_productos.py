import sqlite3

productos = [
    ("Conjunto de encaje negro", 12000, "conjunto1.jpg"),
    ("Body de satén rojo", 15000, "body1.jpg"),
    ("Corpiño push-up", 9800, "corpinio1.jpg")
]

conn = sqlite3.connect("lenceria.db")
cursor = conn.cursor()

cursor.executemany(
    "INSERT INTO productos (nombre, precio, imagen) VALUES (?, ?, ?)",
    productos
)

conn.commit()
conn.close()

print("Productos cargados correctamente")
