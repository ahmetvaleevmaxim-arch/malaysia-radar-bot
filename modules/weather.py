import requests

from config import CITIES


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

    66: "🌧 Ледяной дождь",
    67: "🌧 Ледяной дождь",

    71: "❄️ Снег",
    73: "❄️ Снег",
    75: "❄️ Сильный снег",

    80: "🌦 Ливень",
    81: "🌧 Ливень",
    82: "⛈ Сильный ливень",

    95: "⛈ Гроза",
    96: "⛈ Гроза с градом",
    99: "⛈ Сильная гроза"
}


def weather_name(code: int) -> str:
    return WEATHER_CODES.get(code, "Неизвестно")


def load_weather(lat, lon):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,"
        "wind_speed_10m,weather_code"
        "&hourly=temperature_2m,weather_code,precipitation_probability"
        "&forecast_days=1"
        "&timezone=Asia%2FKuala_Lumpur"
    )

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        return response.json()

    except Exception:

        return None


def city_weather(city, data):

    weather = load_weather(
        data["lat"],
        data["lon"]
    )

    if weather is None:
        return (
            f"📍 {city}\n"
            "Не удалось получить погоду.\n"
        )

    current = weather["current"]

    hourly = weather["hourly"]

    temperature = current["temperature_2m"]

    humidity = current["relative_humidity_2m"]

    wind = current["wind_speed_10m"]

    code = current["weather_code"]

    text = []

    text.append(f"📍 {city}")

    text.append(f"Сейчас: {weather_name(code)}")

    text.append(f"🌡 Температура: {temperature}°C")

    text.append(f"💧 Влажность: {humidity}%")

    text.append(f"💨 Ветер: {wind} км/ч")

    text.append("")

    text.append("Прогноз на ближайшие 3 часа:")

    for i in range(3):

        hour = hourly["time"][i][-5:]

        temp = hourly["temperature_2m"][i]

        rain = hourly["precipitation_probability"][i]

        code = hourly["weather_code"][i]

        text.append(
            f"{hour} | "
            f"{temp}°C | "
            f"{weather_name(code)} | "
            f"🌧 {rain}%"
        )

    return "\n".join(text)


def format_weather():

    report = []

    report.append("🌦 Погода")

    report.append("━━━━━━━━━━━━━━━━━━")

    report.append("")

    for city, data in CITIES.items():

        report.append(city_weather(city, data))

        report.append("")

    return "\n".join(report)
