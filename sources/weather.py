from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

from config import CITIES
from core.models import RadarEvent


API = "https://api.open-meteo.com/v1/forecast"
MY_TIMEZONE = ZoneInfo("Asia/Kuala_Lumpur")


WEATHER_CODES = {
    0: "ясно",
    1: "малооблачно",
    2: "переменная облачность",
    3: "пасмурно",
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


def weather_name(code) -> str:
    try:
        return WEATHER_CODES.get(int(code), "неизвестно")
    except Exception:
        return "неизвестно"


def now_myt() -> datetime:
    return datetime.now(MY_TIMEZONE)


def fetch_weather(city: str):
    data = CITIES[city]

    params = {
        "latitude": data["lat"],
        "longitude": data["lon"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "hourly": "temperature_2m,weather_code,precipitation_probability",
        "forecast_days": 1,
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
            rain = hourly.get("precipitation_probability", [])

            current_text = (
                f"Сейчас: {current.get('temperature_2m')}°C, "
                f"{weather_name(current.get('weather_code'))}, "
                f"влажность {current.get('relative_humidity_2m')}%, "
                f"ветер {current.get('wind_speed_10m')} км/ч."
            )

            forecast_lines = []

            for h in [1, 2, 3]:
                target = now + timedelta(hours=h)
                idx = find_hour_index(times, target)

                if idx is None:
                    continue

                time_value = times[idx][-5:]
                temp = temps[idx] if idx < len(temps) else "—"
                code = codes[idx] if idx < len(codes) else None
                rain_prob = rain[idx] if idx < len(rain) else "—"

                forecast_lines.append(
                    f"+{h} час ({time_value} MYT): "
                    f"{temp}°C, {weather_name(code)}, дождь {rain_prob}%"
                )

            summary = current_text + "\n" + "\n".join(forecast_lines)

            priority = 2
            text_low = summary.lower()

            if "гроза" in text_low or "сильный дождь" in text_low or "ливень" in text_low:
                priority = 4

            events.append(
                RadarEvent(
                    event_type="weather",
                    city=city,
                    title=f"Погода в {city}",
                    summary=summary,
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
