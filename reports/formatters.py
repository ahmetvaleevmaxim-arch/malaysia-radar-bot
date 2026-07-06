from core.models import RadarEvent
from core.text import click, ru_title, short_text, translate_to_ru


def priority_icon(priority: int) -> str:
    if priority >= 5:
        return "🔴"
    if priority >= 4:
        return "🟠"
    if priority >= 3:
        return "🟡"
    return "🟢"


def event_line(event: RadarEvent, index: int | None = None) -> str:
    prefix = f"{index}. " if index else ""
    icon = priority_icon(event.priority)

    title = ru_title(event.title, limit=100)

    if event.url:
        return f'{prefix}{icon} {title} — {click(event.url)}'

    return f"{prefix}{icon} {title}"


def event_block(event: RadarEvent) -> str:
    icon = priority_icon(event.priority)
    title = ru_title(event.title, limit=100)

    lines = [
        f"{icon} {title}",
    ]

    if event.city and event.event_type != "weather":
        lines.append(f"Город: {event.city}")

    if event.company:
        lines.append(f"Компания: {event.company}")

    if event.category:
        lines.append(f"Категория: {event.category}")

    if event.summary:
        lines.append(event.summary)

    if event.url:
        lines.append(f"Ссылка: {click(event.url)}")

    return "\n".join(lines)
