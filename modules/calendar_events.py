import json
from datetime import date, timedelta
from pathlib import Path

DATA_FILE = Path("data/events.json")


def load_events():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def upcoming_events(days_ahead: int = 14):
    today = date.today()
    limit = today + timedelta(days=days_ahead)
    result = []

    for event in load_events():
        try:
            event_date = date.fromisoformat(event["date"])
        except Exception:
            continue

        if today <= event_date <= limit:
            event = dict(event)
            event["days_left"] = (event_date - today).days
            result.append(event)

    return sorted(result, key=lambda item: item["date"])


def format_calendar(days_ahead: int = 14):
    events = upcoming_events(days_ahead)

    lines = [f"📅 Календарь на ближайшие {days_ahead} дней\n"]

    if not events:
        lines.append("Событий не найдено.")
        return "\n".join(lines)

    for event in events:
        days_left = event["days_left"]
        if days_left == 0:
            when = "сегодня"
        elif days_left == 1:
            when = "завтра"
        else:
            when = f"через {days_left} дн."

        lines.append(
            f"• {event['date']} — {when}\n"
            f"  📍 {event.get('city', 'Malaysia')}\n"
            f"  {event.get('title')}\n"
            f"  Тип: {event.get('type', 'event')}\n"
            f"  Важность: {event.get('importance', 'normal')}\n"
        )

    return "\n".join(lines)
