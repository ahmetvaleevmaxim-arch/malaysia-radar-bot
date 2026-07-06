from services.holiday_service import get_calendar


def format_calendar() -> str:
    calendar = get_calendar()

    holidays = calendar.get("holidays", [])
    events = calendar.get("events", [])

    lines = [
        "📅 Праздники и мероприятия",
        "━━━━━━━━━━━━━━━━━━",
        ""
    ]

    lines.append("🇲🇾 Ближайшие праздники")
    lines.append("")

    if not holidays:
        lines.append("Праздников не найдено.")
    else:
        for holiday in holidays:
            lines.append(
                f"📅 {holiday['date']} | {holiday['city']}"
            )
            lines.append(f"{holiday['title']}")
            lines.append(f"До события: {holiday['days_left']} дн.")

            if holiday.get("note"):
                lines.append(holiday["note"])

            lines.append("")

    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append("")
    lines.append("🎉 Ближайшие мероприятия")
    lines.append("")

    if not events:
        lines.append("Мероприятий не найдено.")
    else:
        for event in events:
            lines.append(
                f"🎉 {event['date']} | {event['city']}"
            )
            lines.append(event["title"])
            lines.append(f"До события: {event['days_left']} дн.")

            if event.get("note"):
                lines.append(event["note"])

            lines.append("")

    return "\n".join(lines)
