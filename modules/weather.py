from datetime import datetime
from zoneinfo import ZoneInfo

from services.weather_service import get_all_weather, get_next_3_hour_indexes


MY_TIMEZONE = ZoneInfo("Asia/Kuala_Lumpur")


WEATHER_CODES = {
    0: "☀️ Ясно",
    1: "🌤 Малооблачно",
    2: "⛅ Переменная облачность",
    3: "☁️ Пасмурно",
    45: "🌫 Туман",
    48: "🌫 Сильный туман",
    51: "🌦 Морось",
    53: "🌦 Морось",
    55: "🌦 Сильная морось",
    61: "🌧 Дождь",
    63: "🌧 Дождь",
    65: "🌧 Сильный дождь",
    80: "🌦 Ливень",
    81: "🌧 Ливень",
    82: "⛈ Сильный ливень",
    95: "⛈ Гроза",
    96: "⛈ Гроза с градом",
    99: "⛈ Сильная гроза",
}


def weather_name(code) -> str:
    try:
        return WEATHER_CODES.get(int(code), "Неизвестно")
    except Exception:
        return "Неизвестно"


def format_weather() -> str:
    data = get_all_weather()
    now = datetime.now(MY_TIMEZONE).strftime("%H:%M")

    lines = [
        "🌦 Погода по городам",
        "━━━━━━━━━━━━━━━━━━",
        f"Время: {now} MYT",
        ""
    ]

    for city, weather in data.items():
        lines.append(f"📍 {city}")

        if weather is None:
            lines.append("Не удалось получить погоду.")
            lines.append("")
            continue

        current = weather.get("current", {})
        hourly = weather.get("hourly", {})

        times = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        codes = hourly.get("weather_code", [])
        rain = hourly.get("precipitation_probability", [])

        lines.append("Сейчас:")
        lines.append(f"{weather_name(current.get('weather_code'))}")
        lines.append(f"🌡 Температура: {current.get('temperature_2m')}°C")
        lines.append(f"💧 Влажность: {current.get('relative_humidity_2m')}%")
        lines.append(f"💨 Ветер: {current.get('wind_speed_10m')} км/ч")
        lines.append("")

        lines.append("Прогноз на ближайшие 3 часа:")

        indexes = get_next_3_hour_indexes(times)

        for label, index in indexes[1:]:
            if index is None:
                lines.append(f"{label}: данных нет")
                continue

            time_value = times[index][-5:] if index < len(times) else "—"
            temp = temps[index] if index < len(temps) else "—"
            code = codes[index] if index < len(codes) else None
            rain_prob = rain[index] if index < len(rain) else "—"

            lines.append(
                f"{label} ({time_value} MYT): "
                f"{temp}°C | {weather_name(code)} | дождь {rain_prob}%"
            )

        lines.append("")

    return "\n".join(lines)
