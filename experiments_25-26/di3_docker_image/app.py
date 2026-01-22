from flask import Flask, request, jsonify
from datetime import datetime
import socket
import os
import random
import platform

app = Flask(__name__)

TIPS = [
    "docker ps toont running containers",
    "docker logs <name> toont output",
    "docker exec -it <name> sh voor inside container",
    "docker inspect <name> voor details",
    "docker rm -f <name> om op te ruimen"
]

def base_info():
    return {
        "container": socket.gethostname(),
        "client_ip": request.remote_addr,
        "time_iso": datetime.now().isoformat(timespec="seconds"),
        "user": os.getenv("USER", "unknown"),
        "python": platform.python_version(),
    }

@app.route("/")
def home():
    info = base_info()
    tip = random.choice(TIPS)

    return f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>di3 Docker Web App</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background: #0f172a;
      color: #e5e7eb;
      margin: 0;
      padding: 0;
    }}
    header {{
      padding: 18px 22px;
      background: #020617;
      border-bottom: 1px solid rgba(255,255,255,.08);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .badge {{
      font-size: 12px;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(34,197,94,.15);
      color: #22c55e;
      border: 1px solid rgba(34,197,94,.25);
    }}
    .wrap {{
      max-width: 900px;
      margin: 22px auto;
      padding: 0 18px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 14px;
    }}
    .card {{
      background: #020617;
      border: 1px solid rgba(255,255,255,.08);
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 10px 25px rgba(0,0,0,.35);
    }}
    h1 {{
      font-size: 18px;
      margin: 0;
    }}
    h2 {{
      font-size: 14px;
      margin: 0 0 10px 0;
      color: #93c5fd;
      font-weight: 700;
      letter-spacing: .3px;
      text-transform: uppercase;
    }}
    code {{
      background: rgba(56,189,248,.12);
      color: #38bdf8;
      padding: 2px 6px;
      border-radius: 6px;
      font-size: 13px;
    }}
    a {{
      color: #a5b4fc;
      text-decoration: none;
    }}
    a:hover {{ text-decoration: underline; }}
    .live {{
      font-size: 22px;
      font-weight: 700;
      color: #22c55e;
      margin-top: 6px;
    }}
    .muted {{ color: rgba(229,231,235,.75); }}
    .row {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 10px;
    }}
    .pill {{
      background: rgba(255,255,255,.06);
      border: 1px solid rgba(255,255,255,.08);
      border-radius: 999px;
      padding: 6px 10px;
      font-size: 12px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>di3 Docker Web App</h1>
    <span class="badge">RUNNING • port 8080</span>
  </header>

  <div class="wrap">
    <div class="grid">
      <div class="card">
        <h2>Live time</h2>
        <div class="live" id="clock"></div>
        <div class="muted">Server time (initial): <code>{info["time_iso"]}</code></div>
      </div>

      <div class="card">
        <h2>Container</h2>
        <p>Container ID: <code>{info["container"]}</code></p>
        <p>Client IP: <code>{info["client_ip"]}</code></p>
        <div class="row">
          <span class="pill">Python {info["python"]}</span>
          <span class="pill">User {info["user"]}</span>
        </div>
      </div>

      <div class="card">
        <h2>Quick actions</h2>
        <p><a href="/health">/health</a> (simple health check)</p>
        <p><a href="/info">/info</a> (json info)</p>
        <p class="muted">Tip: <code>{tip}</code></p>
      </div>
    </div>
  </div>

  <script>
    function tick() {{
      const now = new Date();
      document.getElementById("clock").textContent =
        now.toLocaleDateString() + " " + now.toLocaleTimeString();
    }}
    tick();
    setInterval(tick, 1000);
  </script>
</body>
</html>
"""

@app.route("/health")
def health():
    return "ok"

@app.route("/info")
def info():
    return jsonify(base_info())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

