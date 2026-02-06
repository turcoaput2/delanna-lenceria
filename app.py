from flask import Flask, render_template, request, redirect, session
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "delanna_secret"

UPLOAD_FOLDER = "static/img"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def get_db():
    conn = sqlite3.connect("tienda.db")
    conn.row_factory = sqlite3.Row
    return conn

# ----------- TIENDA -----------

@app.route("/")
def index():
    db = get_db()
    productos = db.execute("SELECT * FROM productos").fetchall()
    db.close()
    return render_template("index.html", productos=productos)

@app.route("/producto/<int:id>")
def producto(id):
    db = get_db()
    producto = db.execute(
        "SELECT * FROM productos WHERE id = ?", (id,)
    ).fetchone()
    db.close()
    return render_template("producto.html", producto=producto)

# ----------- LOGIN -----------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]

        if user == "delfiligorria" and password == "delanna590":
            session["admin"] = True
            return redirect("/admin")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")

# ----------- ADMIN -----------

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect("/login")

    db = get_db()

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        imagen = request.files["imagen"]

        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        db.execute(
            "INSERT INTO productos (nombre, precio, imagen) VALUES (?, ?, ?)",
            (nombre, precio, filename)
        )
        db.commit()

    productos = db.execute("SELECT * FROM productos").fetchall()
    db.close()

    return render_template("admin.html", productos=productos)

# ----------- EDITAR / ELIMINAR -----------

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if not session.get("admin"):
        return redirect("/login")

    db = get_db()

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]

        db.execute(
            "UPDATE productos SET nombre=?, precio=? WHERE id=?",
            (nombre, precio, id)
        )
        db.commit()
        db.close()
        return redirect("/admin")

    producto = db.execute(
        "SELECT * FROM productos WHERE id=?", (id,)
    ).fetchone()
    db.close()

    return render_template("editar.html", producto=producto)

@app.route("/eliminar/<int:id>")
def eliminar(id):
    if not session.get("admin"):
        return redirect("/login")

    db = get_db()
    db.execute("DELETE FROM productos WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect("/admin")

# ----------- CARRITO -----------

@app.route("/agregar/<int:id>")
def agregar(id):
    carrito = session.get("carrito", [])
    carrito.append(id)
    session["carrito"] = carrito
    return redirect("/")

@app.route("/carrito")
def carrito():
    ids = session.get("carrito", [])
    db = get_db()

    productos = []
    for i in ids:
        p = db.execute(
            "SELECT * FROM productos WHERE id=?", (i,)
        ).fetchone()
        if p:
            productos.append(p)

    db.close()
    return render_template("carrito.html", productos=productos)

# -----------

if __name__ == "__main__":
    app.run(debug=True)

