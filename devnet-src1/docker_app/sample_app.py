from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import datetime
import sqlite3
import requests
import bcrypt

app = Flask(__name__)
app.secret_key = "super-secret-key"  # nodig voor flash() / sessies light

DB_PATH = "users.db"

# -----------------------
# DB helpers
# -----------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # oude tabel droppen om schema-fouten te vermijden
    cur.execute("DROP TABLE IF EXISTS users")

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()

# -----------------------
# Weather helpers
# -----------------------
API_KEY = "680790fd16e648b6902141454250412"
CURRENT_WEATHER_URL = "http://api.weatherapi.com/v1/current.json"
FORECAST_URL = "http://api.weatherapi.com/v1/forecast.json"
CITY = "Brussels"


def get_weather():
    params = {"key": API_KEY, "q": CITY, "aqi": "no"}
    r = requests.get(CURRENT_WEATHER_URL, params=params)
    r.raise_for_status()
    return r.json()


def get_forecast():
    params = {"key": API_KEY, "q": CITY, "days": 3, "aqi": "no", "alerts": "no"}
    r = requests.get(FORECAST_URL, params=params)
    r.raise_for_status()
    data = r.json()
    if "forecast" in data and "forecastday" in data["forecast"]:
        return data["forecast"]["forecastday"]
    return []


# -----------------------
# Navbar snippet (alleen HTML)
# -----------------------
NAV = """
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">DockerApp</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto">
        <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="/time">Tijd</a></li>
        <li class="nav-item"><a class="nav-link" href="/map">Mijn Locatie</a></li>
        <li class="nav-item"><a class="nav-link" href="/weather">Weather</a></li>
        <li class="nav-item"><a class="nav-link" href="/login">Login</a></li>
        <li class="nav-item"><a class="nav-link" href="/register">Register</a></li>
      </ul>
    </div>
  </div>
</nav>
"""


# -----------------------
# Basis pagina's
# -----------------------
@app.route("/")
def home():
    return render_template("index.html", nav=NAV)


@app.route("/time")
def time_page():
    return render_template("time.html", nav=NAV)


@app.route("/map")
def map_page():
    return render_template("map.html", nav=NAV)


@app.route("/weather")
def weather_page():
    return render_template(
        "weather.html",
        nav=NAV,
        current=get_weather(),
        daily=get_forecast(),
    )


@app.route("/api/time")
def api_time():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"time": now})


# -----------------------
# LOGIN + REGISTER (bcrypt)
# -----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Vul zowel gebruikersnaam als wachtwoord in.")
            return redirect(url_for("login"))

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()

        if row is None:
            flash("Gebruiker bestaat niet.")
            return redirect(url_for("login"))

        stored_hash = row["password_hash"].encode("utf-8")
        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            flash("Fout wachtwoord.")
            return redirect(url_for("login"))

        flash(f"Ingelogd als {username}.")
        return redirect(url_for("home"))

    return render_template("login.html", nav=NAV)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Vul zowel gebruikersnaam als wachtwoord in.")
            return redirect(url_for("register"))

        # bcrypt hash
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                 "CREATE TABLE IF NOT EXISTS USER_PLAIN (USERNAME TEXT PRIMARY KEY NOT NULL, PASSWORD TEXT NOT NULL); "
            )
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, pw_hash),
            )
            conn.commit()
            conn.close()
            flash("Registratie geslaagd. Je kan nu inloggen.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            conn.close()
            flash("Gebruikersnaam bestaat al.")
            return redirect(url_for("register"))

    return render_template("register.html", nav=NAV)


# -----------------------
# Main (voor Docker)
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, threaded=False)
