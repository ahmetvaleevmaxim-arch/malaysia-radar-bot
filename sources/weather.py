from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

from config import CITIES
from core.models import RadarEvent


API = "https://api.open-meteo.com/v1/forecast"
MY_TIMEZONE = ZoneInfo("Asia/Kuala_Lumpur")


WEATHER_CODES = {
    0: "солнечно",
    1: "малооблачно",
    2: "переменная облачность",
    3: "облачно без осадков",
    45: "туман",
    48: "сильный туман",
    51: "морось",
    53: "морось",
    55: "сильная морось",
    61: "дождь",
    63: "дождь",
    65: "сильный дождь",
    80: "ливень",
    81: "ливень",
    82: "сильный ливень",
    95: "гроза",
    96: "гроза с градом",
    99: "сильная гроза",
}


PRECIPITATION_CODES = {
    51, 53, 55,
    61, 63, 65,
    80, 81, 82,
    95, 96, 99,
}


def weather_name(code) -> str:
    try:
        return WEATHER_CODES.get(int(code), "погода неизвестна")
    except Exception:
        return "погода неизвестна"


def is_precipitation(code) -> bool:
    try:
        return int(code) in PRECIPITATION_CODES
    except Exception:
        return False


def format_condition(code, wind_speed=None) -> str:
    name = weather_name(code)

    if is_precipitation(code):
        if wind_speed is not None and wind_speed >= 25:
            return f"❗ {name} с сильным ветром"

        return f"❗ {name}"

    return name


def now_myt() -> datetime:
    return datetime.now(MY_TIMEZONE)


def fetch_weather(city: str):
    data = CITIES[city]

    params = {
        "latitude": data["lat"],
        "longitude": data["lon"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "hourly": "temperature_2m,weather_code,wind_speed_10m",
        "forecast_days": 2,
        "timezone": "Asia/Kuala_Lumpur",
    }

    response = requests.get(API, params=params, timeout=20)
    response.raise_for_status()

    return response.json()


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


def collect_weather_events() -> list[RadarEvent]:
    events = []
    now = now_myt()

    for city in CITIES:
        try:
            weather = fetch_weather(city)

            current = weather.get("current", {})
            hourly = weather.get("hourly", {})

            times = hourly.get("time", [])
            temps = hourly.get("temperature_2m", [])
            codes = hourly.get("weather_code", [])
            winds = hourly.get("wind_speed_10m", [])

            current_code = current.get("weather_code")
            current_temp = current.get("temperature_2m")
            current_humidity = current.get("relative_humidity_2m")
            current_wind = current.get("wind_speed_10m")

            summary_lines = [
                "Сейчас:",
                f"{current_temp}°C, {format_condition(current_code, current_wind)}",
                f"Влажность: {current_humidity}%",
                f"Ветер: {current_wind} км/ч",
                "",
                "Ближайшие 6 часов:",
            ]

            has_bad_weather = is_precipitation(current_code)

            for h in range(1, 7):
                target = now + timedelta(hours=h)
                idx = find_hour_index(times, target)

                if idx is None:
                    continue

                time_value = times[idx][-5:]
                temp = temps[idx] if idx < len(temps) else "—"
                code = codes[idx] if idx < len(codes) else None
                wind = winds[idx] if idx < len(winds) else None

                condition = format_condition(code, wind)

                if is_precipitation(code):
                    has_bad_weather = True

                summary_lines.append(
                    f"+{h} час ({time_value} MYT): {temp}°C, {condition}"
                )

            priority = 4 if has_bad_weather else 2

            events.append(
                RadarEvent(
                    event_type="weather",
                    city=city,
                    title=f"Погода в {city}",
                    summary="\n".join(summary_lines),
                    source="Open-Meteo",
                    priority=priority,
                )
            )

        except Exception:
            events.append(
                RadarEvent(
                    event_type="weather",
                    city=city,
                    title=f"Погода в {city}",
                    summary="Не удалось получить данные о погоде.",
                    source="Open-Meteo",
                    priority=1,
                )
            )

    return events
