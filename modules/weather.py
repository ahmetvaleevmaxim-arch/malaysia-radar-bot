from services.weather_service import get_all_weather


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

    lines = [
        "🌦 Погода по городам",
        "━━━━━━━━━━━━━━━━━━",
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

        code = current.get("weather_code")

        lines.append(f"Сейчас: {weather_name(code)}")
        lines.append(f"🌡 Температура: {current.get('temperature_2m')}°C")
        lines.append(f"💧 Влажность: {current.get('relative_humidity_2m')}%")
        lines.append(f"💨 Ветер: {current.get('wind_speed_10m')} км/ч")
        lines.append("")
        lines.append("Прогноз на ближайшие 3 часа:")

        times = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        codes = hourly.get("weather_code", [])
        rain = hourly.get("precipitation_probability", [])

        for i in range(min(3, len(times))):
            hour = times[i][-5:] if times[i] else "—"
            temp = temps[i] if i < len(temps) else "—"
            weather_code = codes[i] if i < len(codes) else None
            rain_prob = rain[i] if i < len(rain) else "—"

            lines.append(
                f"{hour} | {temp}°C | {weather_name(weather_code)} | 🌧 {rain_prob}%"
            )

        lines.append("")

    return "\n".join(lines)
