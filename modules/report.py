from modules.weather import collect_weather
from modules.currency import collect_currency
from modules.news import collect_news
from modules.calendar_events import upcoming_events
from modules.utils import now_myt


def build_daily_report():
    now = now_myt()
    weather = collect_weather()
    news = collect_news()
    events = upcoming_events(14)

    try:
        currency = collect_currency()
    except Exception:
        currency = {}

    lines = [
        f"🇲🇾 Malaysia Radar Daily Report",
        f"Дата: {now.strftime('%d.%m.%Y')}",
        f"Время: {now.strftime('%H:%M')} MYT",
        "",
        "━━━━━━━━━━━━━━",
        "1. Главное",
        "━━━━━━━━━━━━━━",
    ]

    warning_count = 0
    for city, item in weather.items():
        if item.get("daily_precipitation") and item["daily_precipitation"] >= 10:
            warning_count += 1

    if warning_count:
        lines.append(f"⚠️ Погодные риски: {warning_count} город(а).")
    else:
        lines.append("✅ Критичных погодных рисков не найдено.")

    if events:
        lines.append(f"📅 Событий в ближайшие 14 дней: {len(events)}.")
    else:
        lines.append("📅 Ближайших событий в календаре нет.")

    lines.extend(["", "━━━━━━━━━━━━━━", "2. Новости Малайзии", "━━━━━━━━━━━━━━"])
    for item in news.get("Malaysia", [])[:5]:
        lines.append(f"• {item['title']}\n  {item['link']}")

    lines.extend(["", "━━━━━━━━━━━━━━", "3. Новости по городам", "━━━━━━━━━━━━━━"])
    for city in ["Miri", "Bintulu", "Labuan", "Sibu", "Seremban"]:
        lines.append(f"\n📍 {city}")
        city_news = news.get(city, [])
        if city_news:
            for item in city_news[:3]:
                lines.append(f"• {item['title']}\n  {item['link']}")
        else:
            lines.append("Локальных новостей не найдено.")

    lines.extend(["", "━━━━━━━━━━━━━━", "4. Погода", "━━━━━━━━━━━━━━"])
    for city, item in weather.items():
        if "error" in item:
            lines.append(f"📍 {city}: ошибка получения данных")
            continue

        impact = "без явного влияния"
        precipitation = item.get("daily_precipitation") or 0
        if precipitation >= 10:
            impact = "возможен рост спроса и задержки"
        elif precipitation >= 3:
            impact = "возможен умеренный рост спроса"

        lines.append(
            f"📍 {city}: {item.get('temperature')}°C, {item.get('description')}; "
            f"осадки за день {item.get('daily_precipitation')} мм; {impact}."
        )

    lines.extend(["", "━━━━━━━━━━━━━━", "5. Валюта", "━━━━━━━━━━━━━━"])
    if currency:
        lines.append(f"1 MYR = {currency.get('MYR_USD')} USD")
        lines.append(f"1 MYR = {currency.get('MYR_RUB')} RUB")
        lines.append(f"1 MYR = {currency.get('MYR_SGD')} SGD")
    else:
        lines.append("Курсы валют не получены.")

    lines.extend(["", "━━━━━━━━━━━━━━", "6. Календарь", "━━━━━━━━━━━━━━"])
    if events:
        for event in events[:8]:
            days_left = event["days_left"]
            when = "сегодня" if days_left == 0 else "завтра" if days_left == 1 else f"через {days_left} дн."
            lines.append(f"• {event['date']} — {when}: {event.get('title')} ({event.get('city')})")
    else:
        lines.append("Событий нет.")

    lines.extend(["", "━━━━━━━━━━━━━━", "7. Что проверить сегодня", "━━━━━━━━━━━━━━"])
    lines.append("• Проверить локальные события по городам.")
    lines.append("• Проверить погоду в городах с осадками.")
    lines.append("• Проверить новости APAD/LPKP вручную, если нужен юридический мониторинг.")

    return "\n".join(lines)
