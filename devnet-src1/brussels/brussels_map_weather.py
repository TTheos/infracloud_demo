from flask import Flask, render_template
import requests

weather_brussels = Flask(__name__)

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
    """Veilige forecast-oproep (crasht nooit)."""
    try:
        params = {
            "key": API_KEY,
            "q": CITY,
            "days": 3,
            "aqi": "no",
            "alerts": "no"
        }
        r = requests.get(FORECAST_URL, params=params)
        r.raise_for_status()

        data = r.json()

        if "forecast" in data and "forecastday" in data["forecast"]:
            return data["forecast"]["forecastday"]

        print("⚠️ Forecast ontbreekt:", data)
        return []

    except Exception as e:
        print("⚠️ Forecast error:", e)
        return []


@weather_brussels.route("/")
def map_page():
    weather = get_weather()
    return render_template(
        "map.html",
        temp=weather["current"]["temp_c"],
        condition=weather["current"]["condition"]["text"],
        icon=weather["current"]["condition"]["icon"]
    )


@weather_brussels.route("/weather")
def weather_page():
    current = get_weather()
    daily = get_forecast()

    return render_template(
        "weather.html",
        current=current,
        daily=daily
    )


if __name__ == "__main__":
    weather_brussels.run(debug=True, host="0.0.0.0", port=5555)
