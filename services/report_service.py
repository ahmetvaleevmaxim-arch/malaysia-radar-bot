from datetime import datetime

from services.news_service import collect_country_news, collect_all_city_news, translate_to_ru, shorten
from services.weather_service import get_all_weather
from services.currency_service import get_currency_rates
from services.competitor_service import get_all_competitors
from services.maxim_service import get_maxim_mentions
from services.holiday_service import get_calendar


def format_news_item(item: dict, index: int) -> str:
    title = translate_to_ru(item.get("title", ""))
    summary = translate_to_ru(shorten(item.get("summary", "")))
    url = item.get("url", "")

    text = f"{index}. {title}\n"

    if summary:
        text += f"{summary}\n"

    if url:
        text += f"Ссылка: {url}\n"

    return text


def build_report() -> str:
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    lines = [
        "🇲🇾 Malaysia Radar",
        "📊 Ежедневный отчет",
        f"Обновлено: {now}",
        "",
        "━━━━━━━━━━━━━━━━━━",
        ""
    ]

    lines.append("📰 Новости по Малайзии")
    lines.append("")

    country_news = collect_country_news()

    if not country_news:
        lines.append("Новости не найдены.")
    else:
        for i, item in enumerate(country_news, 1):
            lines.append(format_news_item(item, i))

    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append("")
    lines.append("📍 Новости по городам")
    lines.append("")

    city_news = collect_all_city_news()

    for city, items in city_news.items():
        lines.append(f"📍 {city}")
        lines.append("")

        if not items:
            lines.append("Новостей не найдено.")
            lines.append("")
            continue

        for i, item in enumerate(items, 1):
            lines.append(format_news_item(item, i))

        lines.append("")

    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append("")
    lines.append("🌦 Погода")
    lines.append("")

    weather = get_all_weather()

    for city, data in weather.items():
        lines.append(f"📍 {city}")

        if data is None:
            lines.append("Не удалось получить погоду.")
            lines.append("")
            continue

        current = data.get("current", {})
        hourly = data.get("hourly", {})

        lines.append(f"Сейчас: {current.get('temperature_2m')}°C")
        lines.append(f"Влажность: {current.get('relative_humidity_2m')}%")
        lines.append(f"Ветер: {current.get('wind_speed_10m')} км/ч")
        lines.append("Прогноз на 3 часа:")

        for i in range(3):
            time_value = hourly.get("time", [""] * 3)[i][-5:]
            temp = hourly.get("temperature_2m", [""] * 3)[i]
            rain = hourly.get("precipitation_probability", [""] * 3)[i]

            lines.append(f"{time_value}: {temp}°C, дождь {rain}%")

        lines.append("")

    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append("")
    lines.append("💰 Валюты")
    lines.append("")

    rates = get_currency_rates()

    if rates is None:
        lines.append("Не удалось получить курсы валют.")
    else:
        lines.append(f"USD → MYR: {rates['USD']}")
        lines.append(f"EUR → MYR: {rates['EUR']}")
        lines.append(f"RUB → MYR: {rates['RUB']}")
        lines.append(f"CNY → MYR: {rates['CNY']}")

    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append("")
    lines.append("🚗 Конкуренты")
    lines.append("")

    competitors = get_all_competitors()

    for company, items in competitors.items():
        lines.append(f"🚗 {company}")

        if not items:
            lines.append("Новостей не найдено.")
            lines.append("")
            continue

        for i, item in enumerate(items, 1):
            lines.append(format_news_item(item, i))

        lines.append("")

    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append("")
    lines.append("🚨 Упоминания Maxim")
    lines.append("")

    mentions = get_maxim_mentions()

    if not mentions:
        lines.append("Упоминаний не найдено.")
    else:
        for i, item in enumerate(mentions, 1):
            category = item.get("category", "упоминание")
            priority = item.get("priority", 0)
            city = item.get("city", "Malaysia")

            lines.append(f"{i}. {category.upper()} | {city} | важность {priority}/5")
            lines.append(format_news_item(item, i))

    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append("")
    lines.append("📅 Праздники и мероприятия")
    lines.append("")

    calendar = get_calendar()

    holidays = calendar.get("holidays", [])
    events = calendar.get("events", [])

    lines.append("Праздники:")
    if not holidays:
        lines.append("На ближайшие 30 дней праздников не найдено.")
    else:
        for item in holidays:
            lines.append(
                f"• {item['date']} — {item['title']} | {item['city']} | через {item['days_left']} дн."
            )

    lines.append("")
    lines.append("Мероприятия:")
    if not events:
        lines.append("На ближайшие 30 дней мероприятий не найдено.")
    else:
        for item in events:
            lines.append(
                f"• {item['date']} — {item['title']} | {item['city']} | через {item['days_left']} дн."
            )

    return "\n".join(lines)
