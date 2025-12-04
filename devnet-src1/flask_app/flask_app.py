from flask import Flask, render_template, request
import datetime
import pytz

microweb_app = Flask(__name__)

# HOME
@microweb_app.route("/")
def main():
    return render_template("index.html")

# SERVER TIME API
@microweb_app.route("/api/time")
def api_time():
    brussels_tz = pytz.timezone("Europe/Brussels")
    now = datetime.datetime.now(brussels_tz)
    return {"time": now.strftime("%Y-%m-%d %H:%M:%S")}

# TIME PAGE
@microweb_app.route("/time")
def time_page():
    return render_template("time.html")

# MAP PAGE
@microweb_app.route("/map")
def map_page():
    return render_template("map.html")

# LOGIN PAGE
@microweb_app.route("/login")
def login_page():
    return render_template("login.html")

# ACCOUNT PAGE
@microweb_app.route("/account")
def account_page():
    return render_template("account.html")

# --------- SERVER BOOT ---------
if __name__ == "__main__":
    microweb_app.run(host="0.0.0.0", port=5555)
