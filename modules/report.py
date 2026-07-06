from datetime import datetime

from modules.news import (
    format_country_news,
    format_city_news,
    format_competitor_news,
    format_maxim_mentions,
)
from modules.weather import format_weather
from modules.currency import format_currency
from modules.calendar_events import format_calendar


def build_daily_report() -> str:
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    parts = [
        "🇲🇾 Malaysia Radar",
        "📊 Ежедневный отчет",
        f"Обновлено: {now}",
        "",
        "━━━━━━━━━━━━━━━━━━",
        "",
        "🎯 Что входит в отчет:",
        "• новости по всей Малайзии",
        "• новости по Miri, Bintulu, Labuan, Sibu, Seremban",
        "• погода по городам и прогноз на 3 часа",
        "• курсы валют",
        "• новости конкурентов",
        "• упоминания Maxim",
        "• праздники и локальные события",
        "",
        "━━━━━━━━━━━━━━━━━━",
        "",
        format_country_news(),
        "",
        format_city_news(),
        "",
        format_weather(),
        "",
        format_currency(),
        "",
        format_competitor_news(),
        "",
        format_maxim_mentions(),
        "",
        format_calendar(),
    ]

    return "\n".join(parts)
