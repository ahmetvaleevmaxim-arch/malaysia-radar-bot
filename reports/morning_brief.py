from core.models import RadarEvent
from core.time import format_myt
from core.constants import CITIES, COMPETITORS
from reports.formatters import event_line, event_block


def section(title: str, items: list[str]) -> list[str]:
    if not items:
        return []

    return [
        title,
        "━━━━━━━━━━━━━━━━━━",
        *items,
        "",
    ]


def build_action_center(events: list[RadarEvent]) -> list[str]:
    important = [event for event in events if event.priority >= 4]
    important.sort(key=lambda event: event.priority, reverse=True)

    lines = []

    for event in important[:10]:
        lines.append(event_line(event))

    if not lines:
        lines.append("🟢 Критичных событий не найдено.")

    return section("🎯 Что требует внимания", lines)


def build_country_news(events: list[RadarEvent]) -> list[str]:
    items = [event for event in events if event.event_type == "country_news"]

    return section(
        "📰 Новости Малайзии за сегодня",
        [event_line(event, i) for i, event in enumerate(items[:10], 1)]
    )


def build_city_news(events: list[RadarEvent]) -> list[str]:
    lines = []

    for city in CITIES:
        city_events = [
            event for event in events
            if event.city == city and event.event_type == "city_news"
        ]

        if not city_events:
            continue

        lines.append(f"📍 {city}")

        for i, event in enumerate(city_events[:5], 1):
            lines.append(event_line(event, i))

        lines.append("")

    return section("📍 Новости городов за сегодня", lines)


def build_competitors(events: list[RadarEvent]) -> list[str]:
    lines = []

    for company in COMPETITORS:
        company_events = [
            event for event in events
            if event.event_type == "competitor" and event.company == company
        ]

        if not company_events:
            continue

        lines.append(f"🚗 {company}")

        for i, event in enumerate(company_events[:5], 1):
            lines.append(event_line(event, i))

        lines.append("")

    return section("🚗 Конкуренты за сегодня", lines)


def build_maxim(events: list[RadarEvent]) -> list[str]:
    items = [event for event in events if event.event_type == "maxim"]

    if not items:
        return section("🚨 Maxim Monitor", ["🟢 Упоминаний за сегодня не найдено."])

    lines = []

    for i, event in enumerate(items[:8], 1):
        lines.append(event_line(event, i))

    return section("🚨 Maxim Monitor", lines)


def build_government(events: list[RadarEvent]) -> list[str]:
    items = [event for event in events if event.event_type == "government"]

    if not items:
        return section("🏛 Государство", ["🟢 Новостей APAD / JPJ / MOT / LPKP / PUSPAKOM за сегодня не найдено."])

    lines = []

    agencies = ["APAD", "JPJ", "MOT", "LPKP", "PUSPAKOM"]

    for agency in agencies:
        agency_events = [event for event in items if event.company == agency]

        if not agency_events:
            continue

        lines.append(f"🏛 {agency}")

        for i, event in enumerate(agency_events[:5], 1):
            lines.append(event_line(event, i))

        lines.append("")

    return section("🏛 Государство", lines)


def build_roads(events: list[RadarEvent]) -> list[str]:
    lines = []

    for city in CITIES:
        city_events = [
            event for event in events
            if event.city == city and event.event_type == "transport"
        ]

        if not city_events:
            continue

        lines.append(f"🛣 {city}")

        for i, event in enumerate(city_events[:5], 1):
            lines.append(event_line(event, i))

        lines.append("")

    if not lines:
        return section("🛣 Дороги", ["🟢 Важных дорожных новостей за сегодня не найдено."])

    return section("🛣 Дороги", lines)


def build_weather(events: list[RadarEvent]) -> list[str]:
    items = [event for event in events if event.event_type == "weather"]

    lines = []

    for event in items:
        lines.append(event_block(event))
        lines.append("")

    return section("🌦 Погода", lines)


def build_currency(events: list[RadarEvent]) -> list[str]:
    items = [event for event in events if event.event_type == "currency"]

    if not items:
        return []

    return section("💰 Валюты", [items[0].summary])


def build_morning_brief(events: list[RadarEvent]) -> str:
    lines = [
        "🇲🇾 Malaysia Radar",
        "🌅 Morning Brief",
        f"Обновлено: {format_myt()}",
        "",
    ]

    lines.extend(build_action_center(events))
    lines.extend(build_country_news(events))
    lines.extend(build_city_news(events))
    lines.extend(build_government(events))
    lines.extend(build_roads(events))
    lines.extend(build_competitors(events))
    lines.extend(build_maxim(events))
    lines.extend(build_weather(events))
    lines.extend(build_currency(events))

    return "\n".join(lines).strip()
