import requests

from config import CITIES


API = (
    "https://api.open-meteo.com/v1/forecast"
)


def get_weather(city: str):

    data = CITIES[city]

    params = {
        "latitude": data["lat"],
        "longitude": data["lon"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "hourly": "temperature_2m,weather_code,precipitation_probability",
        "forecast_days": 1,
        "timezone": "Asia/Kuala_Lumpur"
    }

    r = requests.get(API, params=params, timeout=20)

    r.raise_for_status()

    return r.json()


def get_all_weather():

    weather = {}

    for city in CITIES.keys():

        try:

            weather[city] = get_weather(city)

        except Exception:

            weather[city] = None

    return weather
