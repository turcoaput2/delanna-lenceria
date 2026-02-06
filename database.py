import sqlite3

# Conectar (crea el archivo si no existe)
conn = sqlite3.connect("lenceria.db")

cursor = conn.cursor()

# Crear tabla productos
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    imagen TEXT
)
""")

conn.commit()
conn.close()

print("Base de datos creada correctamente")
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    password TEXT
)
""")
cursor.execute(
    "INSERT INTO admin (usuario, password) VALUES (?, ?)",
    ("delfiligorria", "delanna590")
)
#login admin
from flask import app, redirect, render_template, request, session
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["usuario"]
        pw = request.form["password"]

        conn = sqlite3.connect("lenceria.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM admin WHERE usuario=? AND password=?",
            (user, pw)
        )
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session["admin"] = True
            return redirect("/admin")

    return render_template("login.html")
    