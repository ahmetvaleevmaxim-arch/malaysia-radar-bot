import requests
from config import CITIES


WEATHER_CODES = {
    0: "ясно",
    1: "преимущественно ясно",
    2: "переменная облачность",
    3: "облачно",
    45: "туман",
    48: "изморозь / туман",
    51: "легкая морось",
    53: "морось",
    55: "сильная морось",
    61: "небольшой дождь",
    63: "дождь",
    65: "сильный дождь",
    80: "ливень",
    81: "сильный ливень",
    82: "очень сильный ливень",
    95: "гроза",
    96: "гроза с градом",
    99: "сильная гроза с градом",
}


def collect_weather():
    result = {}

    for city, info in CITIES.items():
        lat = info["lat"]
        lon = info["lon"]

        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,precipitation,rain,weather_code,wind_speed_10m"
            "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
            "&forecast_days=1"
            "&timezone=Asia%2FKuala_Lumpur"
        )

        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            data = response.json()
            current = data.get("current", {})
            daily = data.get("daily", {})

            code = current.get("weather_code")
            result[city] = {
                "temperature": current.get("temperature_2m"),
                "rain": current.get("rain"),
                "precipitation": current.get("precipitation"),
                "wind": current.get("wind_speed_10m"),
                "description": WEATHER_CODES.get(code, f"код погоды {code}"),
                "max_temp": (daily.get("temperature_2m_max") or [None])[0],
                "min_temp": (daily.get("temperature_2m_min") or [None])[0],
                "daily_precipitation": (daily.get("precipitation_sum") or [None])[0],
            }

        except Exception as exc:
            result[city] = {"error": str(exc)}

    return result


def format_weather():
    data = collect_weather()
    lines = ["🌦 Погода по городам Малайзии\n"]

    for city, item in data.items():
        if "error" in item:
            lines.append(f"📍 {city}\nОшибка: {item['error']}\n")
            continue

        impact = "без явного влияния"
        precipitation = item.get("daily_precipitation") or 0
        if precipitation >= 10:
            impact = "возможен рост спроса и задержки подачи"
        elif precipitation >= 3:
            impact = "возможен умеренный рост спроса"

        lines.append(
            f"📍 {city}\n"
            f"Сейчас: {item.get('temperature')}°C, {item.get('description')}\n"
            f"Дождь сейчас: {item.get('rain')} мм\n"
            f"Осадки за день: {item.get('daily_precipitation')} мм\n"
            f"Ветер: {item.get('wind')} км/ч\n"
            f"Влияние: {impact}\n"
        )

    return "\n".join(lines)
