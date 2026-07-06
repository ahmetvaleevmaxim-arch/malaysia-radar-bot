from services.news_service import (
    collect_country_news,
    collect_all_city_news,
    translate_to_ru,
    shorten,
)
from services.competitor_service import get_all_competitors
from services.maxim_service import get_maxim_mentions


def format_item(item: dict, index: int) -> str:
    title = translate_to_ru(item.get("title", ""))
    summary = translate_to_ru(shorten(item.get("summary", "")))

    text = f"{index}. {title}\n"

    if summary:
        text += f"{summary}\n"

    if item.get("source"):
        text += f"Источник: {item.get('source')}\n"

    if item.get("published"):
        text += f"Дата: {item.get('published')}\n"

    if item.get("url"):
        text += f"Ссылка: {item.get('url')}\n"

    return text


def format_country_news() -> str:
    items = collect_country_news()

    lines = [
        "📰 Новости по Малайзии",
        "━━━━━━━━━━━━━━━━━━",
        ""
    ]

    if not items:
        lines.append("Новости не найдены.")
        return "\n".join(lines)

    for i, item in enumerate(items, 1):
        lines.append(format_item(item, i))

    return "\n".join(lines)


def format_city_news() -> str:
    data = collect_all_city_news()

    lines = [
        "📍 Новости по городам",
        "━━━━━━━━━━━━━━━━━━",
        ""
    ]

    for city, items in data.items():
        lines.append(f"📍 {city}")
        lines.append("")

        if not items:
            lines.append("Новостей не найдено.")
            lines.append("")
            continue

        for i, item in enumerate(items, 1):
            lines.append(format_item(item, i))

        lines.append("")

    return "\n".join(lines)


def format_competitor_news() -> str:
    data = get_all_competitors()

    lines = [
        "🚗 Новости конкурентов",
        "━━━━━━━━━━━━━━━━━━",
        ""
    ]

    for company, items in data.items():
        lines.append(f"🚗 {company}")
        lines.append("")

        if not items:
            lines.append("Новостей не найдено.")
            lines.append("")
            continue

        for i, item in enumerate(items, 1):
            lines.append(format_item(item, i))

        lines.append("")

    return "\n".join(lines)


def format_maxim_mentions() -> str:
    items = get_maxim_mentions()

    lines = [
        "🚨 Упоминания Maxim",
        "━━━━━━━━━━━━━━━━━━",
        ""
    ]

    if not items:
        lines.append("Упоминаний не найдено.")
        return "\n".join(lines)

    for i, item in enumerate(items, 1):
        category = item.get("category", "упоминание")
        priority = item.get("priority", 0)
        city = item.get("city", "Malaysia")

        if priority >= 4:
            label = "🔴 Важное упоминание"
        elif category == "негатив":
            label = "🟠 Возможный негатив"
        else:
            label = "🟢 Обычное упоминание"

        lines.append(f"{label} | {city} | важность {priority}/5")
        lines.append(format_item(item, i))

    return "\n".join(lines)


def format_news() -> str:
    return "\n\n".join([
        format_country_news(),
        format_city_news(),
        format_competitor_news(),
        format_maxim_mentions(),
    ])
