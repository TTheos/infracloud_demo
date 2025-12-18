from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib
from datetime import datetime
import os

app = Flask(__name__)

# DB zit in volume (/data)
DB_PATH = "/data/user.db"

# ---------- HELPERS ----------
def get_db():
    return sqlite3.connect(DB_PATH)

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


# ---------- INDEX ----------
@app.route("/")
def index():
    return render_template("index.html")


# ---------- SIGNUP V2 ----------
@app.route("/signup/v2", methods=["GET", "POST"])
def signup_v2():
    if request.method == "GET":
        return render_template("signup.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Missing fields", 400

    db = get_db()
    c = db.cursor()

    try:
        now = datetime.utcnow().isoformat()
        c.execute(
            """
            INSERT INTO USER_PLAIN (USERNAME, PASSWORD, CREATED_AT)
            VALUES (?, ?, ?)
            """,
            (username, hash_password(password), now),
        )
        db.commit()
        return redirect(url_for("login_v2"))
    except sqlite3.IntegrityError:
        return "User already exists", 409
    finally:
        db.close()


# ---------- LOGIN V2 ----------
@app.route("/login/v2", methods=["GET", "POST"])
def login_v2():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    db = get_db()
    c = db.cursor()

    c.execute(
        "SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = ?",
        (username,),
    )
    row = c.fetchone()

    if not row or row[0] != hash_password(password):
        db.close()
        return "Invalid credentials", 401

    now = datetime.utcnow().isoformat()
    c.execute(
        "UPDATE USER_PLAIN SET LAST_LOGIN = ? WHERE USERNAME = ?",
        (now, username),
    )
    db.commit()
    db.close()

    return redirect(url_for("index"))


# ---------- UPDATE PASSWORD V2 ----------
@app.route("/update-pw/v2", methods=["GET", "POST"])
def update_pw_v2():
    if request.method == "GET":
        return render_template("update_password.html")

    username = request.form.get("username")
    old_pw = request.form.get("old_password")
    new_pw = request.form.get("new_password")

    db = get_db()
    c = db.cursor()

    c.execute(
        "SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = ?",
        (username,),
    )
    row = c.fetchone()

    if not row or row[0] != hash_password(old_pw):
        db.close()
        return "Invalid credentials", 401

    now = datetime.utcnow().isoformat()
    c.execute(
        """
        UPDATE USER_PLAIN
        SET PASSWORD = ?, PASSWORD_UPDATED_AT = ?
        WHERE USERNAME = ?
        """,
        (hash_password(new_pw), now, username),
    )

    db.commit()
    db.close()
    return redirect(url_for("login_v2"))


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
