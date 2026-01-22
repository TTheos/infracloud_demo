import requests
import urllib.parse
import os

API_KEY = os.getenv("GRAPHOPPER_KEY")
GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"

def geocode(location):
    while location == "":
        location = input("Enter location again: ")

    url = GEOCODE_URL + urllib.parse.urlencode({
        "q": location,
        "limit": "1",
        "key": API_KEY
    })

    r = requests.get(url)
    data = r.json()

    if r.status_code == 200 and len(data["hits"]) > 0:
        p = data["hits"][0]["point"]
        name = data["hits"][0]["name"]
        country = data["hits"][0].get("country", "")
        state = data["hits"][0].get("state", "")
        label = ", ".join(filter(None, [name, state, country]))
        print(f"Geocoding API URL for {label}\n{url}")
        return p["lat"], p["lng"], label

    print("Geocoding failed")
    return None, None, None


while True:
    print("\ncar, bike, foot")
    vehicle = input("Vehicle: ")
    if vehicle in ["q", "quit"]:
        break
    if vehicle not in ["car", "bike", "foot"]:
        vehicle = "car"

    start = input("Starting Location: ")
    if start in ["q", "quit"]:
        break

    end = input("Destination: ")
    if end in ["q", "quit"]:
        break

    lat1, lng1, name1 = geocode(start)
    lat2, lng2, name2 = geocode(end)

    if None in [lat1, lat2]:
        continue

    route_url = ROUTE_URL + urllib.parse.urlencode({
        "key": API_KEY,
        "vehicle": vehicle
    }) + f"&point={lat1}%2C{lng1}&point={lat2}%2C{lng2}"

    r = requests.get(route_url)
    data = r.json()

    print("=================================================")
    if r.status_code == 200:
        dist_km = data["paths"][0]["distance"] / 1000
        dist_mi = dist_km / 1.61
        t = int(data["paths"][0]["time"] / 1000)
        h, m, s = t // 3600, (t % 3600) // 60, t % 60

        print(f"Directions from {name1} to {name2} by {vehicle}")
        print(f"Distance: {dist_mi:.1f} miles / {dist_km:.1f} km")
        print(f"Duration: {h:02d}:{m:02d}:{s:02d}")
        print("=================================================")

        for step in data["paths"][0]["instructions"]:
            print(f"{step['text']} ( {step['distance']/1000:.1f} km )")
    else:
        print("Routing error:", data.get("message"))

    print("=================================================")
