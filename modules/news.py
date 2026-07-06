from services.news_service import (
    collect_country_news,
    collect_all_city_news,
    make_short_ru_title,
)
from services.competitor_service import get_all_competitors
from services.maxim_service import get_maxim_mentions


def click_link(url: str) -> str:
    if not url:
        return ""

    return f'<a href="{url}">КЛИК</a>'


def format_item(item: dict, index: int) -> str:
    title = make_short_ru_title(item.get("title", ""))
    url = item.get("url", "")

    if url:
        return f'{index}. {title} — {click_link(url)}'

    return f"{index}. {title}"


def format_country_news() -> str:
    items = collect_country_news()

    lines = [
        "📰 Новости по Малайзии за сегодня",
        "━━━━━━━━━━━━━━━━━━",
        ""
    ]

    if not items:
        lines.append("Новостей за сегодня не найдено.")
        return "\n".join(lines)

    for i, item in enumerate(items, 1):
        lines.append(format_item(item, i))

    return "\n".join(lines)


def format_city_news() -> str:
    data = collect_all_city_news()

    lines = [
        "📍 Новости по городам за сегодня",
        "━━━━━━━━━━━━━━━━━━",
        ""
    ]

    for city, items in data.items():
        lines.append(f"📍 {city}")

        if not items:
            lines.append("Новостей за сегодня не найдено.")
            lines.append("")
            continue

        for i, item in enumerate(items, 1):
            lines.append(format_item(item, i))

        lines.append("")

    return "\n".join(lines)


def format_competitor_news() -> str:
    data = get_all_competitors()

    lines = [
        "🚗 Новости конкурентов за сегодня",
        "━━━━━━━━━━━━━━━━━━",
        ""
    ]

    for company, items in data.items():
        lines.append(f"🚗 {company}")

        if not items:
            lines.append("Новостей за сегодня не найдено.")
            lines.append("")
            continue

        for i, item in enumerate(items, 1):
            lines.append(format_item(item, i))

        lines.append("")

    return "\n".join(lines)


def format_maxim_mentions() -> str:
    items = get_maxim_mentions()

    lines = [
        "🚨 Упоминания Maxim e-hailing Malaysia за сегодня",
        "━━━━━━━━━━━━━━━━━━",
        ""
    ]

    if not items:
        lines.append("Упоминаний за сегодня не найдено.")
        return "\n".join(lines)

    for i, item in enumerate(items, 1):
        category = item.get("category", "упоминание")
        priority = item.get("priority", 0)
        city = item.get("city", "Malaysia")
        title = make_short_ru_title(item.get("title", ""))
        url = item.get("url", "")

        if priority >= 4:
            label = "🔴 Важное"
        elif category == "негатив":
            label = "🟠 Негатив"
        else:
            label = "🟢 Упоминание"

        if url:
            lines.append(f'{i}. {label} | {city} | {title} — {click_link(url)}')
        else:
            lines.append(f"{i}. {label} | {city} | {title}")

    return "\n".join(lines)


def format_news() -> str:
    return "\n\n".join([
        format_country_news(),
        format_city_news(),
        format_competitor_news(),
        format_maxim_mentions(),
    ])
