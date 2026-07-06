from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

from config import CITIES


API = "https://api.open-meteo.com/v1/forecast"
MY_TIMEZONE = ZoneInfo("Asia/Kuala_Lumpur")


def malaysia_now() -> datetime:
    return datetime.now(MY_TIMEZONE)


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


def find_hour_index(times: list[str], target: datetime) -> int | None:
    target_hour = target.replace(minute=0, second=0, microsecond=0)

    for i, value in enumerate(times):
        try:
            dt = datetime.fromisoformat(value).replace(tzinfo=MY_TIMEZONE)
            dt = dt.replace(minute=0, second=0, microsecond=0)

            if dt == target_hour:
                return i

        except Exception:
            continue

    return None


def get_next_3_hour_indexes(times: list[str]) -> list[tuple[str, int | None]]:
    now = malaysia_now()

    targets = [
        ("Сейчас", now),
        ("+1 час", now + timedelta(hours=1)),
        ("+2 часа", now + timedelta(hours=2)),
        ("+3 часа", now + timedelta(hours=3)),
    ]

    result = []

    for label, target in targets:
        result.append((label, find_hour_index(times, target)))

    return result
