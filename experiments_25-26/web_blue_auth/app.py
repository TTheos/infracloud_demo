import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

APP_DB = "app.db"

app = Flask(__name__)
app.secret_key = "change-me-in-class"  # ok for lab; not for production


def db():
    conn = sqlite3.connect(APP_DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            pass_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


@app.route("/")
def home():
    user = session.get("user")
    return render_template("home.html", user=user)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if len(username) < 3 or len(password) < 6:
            flash("Username min 3 chars, password min 6 chars.")
            return redirect(url_for("signup"))

        conn = db()
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO users (username, pass_hash, created_at) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), datetime.now().isoformat(timespec="seconds")),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Username bestaat al.")
            conn.close()
            return redirect(url_for("signup"))
        conn.close()

        flash("Account gemaakt. Log nu in.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        conn = db()
        c = conn.cursor()
        c.execute("SELECT username, pass_hash, created_at FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()

        if not row or not check_password_hash(row["pass_hash"], password):
            flash("Foute username/password.")
            return redirect(url_for("login"))

        session["user"] = row["username"]
        session["created_at"] = row["created_at"]
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    return render_template(
        "dashboard.html",
        user=user,
        created_at=session.get("created_at", ""),
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080)
