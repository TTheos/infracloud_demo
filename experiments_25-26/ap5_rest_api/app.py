from flask import Flask, request, jsonify
from datetime import datetime
import os
import platform

app = Flask(__name__)

# ----------------------------
# Homepage (mooier + live time)
# ----------------------------
@app.route("/", methods=["GET"])
def home():
    user = os.getenv("USER") or os.getenv("USERNAME") or "unknown"
    host = platform.node() or "unknown"
    return f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>ap5 – Local REST API</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background: #0f172a;
      color: #e5e7eb;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }}
    .card {{
      background: #020617;
      padding: 24px 32px;
      border-radius: 10px;
      box-shadow: 0 10px 30px rgba(0,0,0,.5);
      width: 420px;
    }}
    h1 {{ margin-top: 0; font-size: 1.4rem; }}
    code {{
      background: #0b1220;
      padding: 2px 6px;
      border-radius: 4px;
      color: #38bdf8;
    }}
    ul {{ padding-left: 18px; }}
    .time {{
      font-size: 1.2rem;
      margin: 10px 0;
      color: #22c55e;
    }}
    a {{ color: #a5b4fc; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>ap5 – Local REST API</h1>

    <div class="time" id="clock"></div>

    <p>User: <code>{user}</code></p>
    <p>Hostname: <code>{host}</code></p>

    <h3>Quick links</h3>
    <ul>
      <li><a href="/time">/time</a></li>
      <li><a href="/whoami">/whoami</a></li>
      <li><a href="/pwd">/pwd</a></li>
      <li><a href="/headers">/headers</a></li>
      <li><a href="/echo?msg=hi">/echo?msg=hi</a></li>
    </ul>
  </div>

  <script>
    function updateClock() {{
      const now = new Date();
      document.getElementById("clock").textContent =
        now.toLocaleDateString() + " " + now.toLocaleTimeString();
    }}
    updateClock();
    setInterval(updateClock, 1000);
  </script>
</body>
</html>
"""

# ----------------------------
# API endpoints
# ----------------------------
@app.route("/time", methods=["GET"])
def time_now():
    return jsonify({
        "iso": datetime.now().isoformat(timespec="seconds"),
        "epoch": int(datetime.now().timestamp())
    })

@app.route("/whoami", methods=["GET"])
def whoami():
    return jsonify({
        "user": os.getenv("USER") or os.getenv("USERNAME"),
        "host": platform.node(),
        "ip_seen": request.remote_addr
    })

@app.route("/pwd", methods=["GET"])
def pwd():
    return jsonify({
        "cwd": os.getcwd(),
        "files": sorted([f for f in os.listdir(".") if not f.startswith(".")])
    })

@app.route("/echo", methods=["GET", "POST"])
def echo():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        return jsonify({"method": "POST", "you_sent": data})
    return jsonify({"method": "GET", "msg": request.args.get("msg", "")})

@app.route("/headers", methods=["GET"])
def headers():
    return jsonify({"headers": dict(request.headers)})

# ----------------------------
# Start server
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
