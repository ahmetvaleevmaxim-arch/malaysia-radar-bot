from datetime import date, datetime, timedelta


LOOKAHEAD_DAYS = 30


HOLIDAYS = [
    {
        "date": "2026-01-01",
        "title": "Новый год",
        "city": "Malaysia",
        "type": "Государственный праздник",
        "note": "Общий выходной день."
    },
    {
        "date": "2026-02-17",
        "title": "Китайский Новый год",
        "city": "Malaysia",
        "type": "Государственный праздник",
        "note": "Может влиять на спрос, поездки и доступность водителей."
    },
    {
        "date": "2026-03-20",
        "title": "Хари Райя Айдильфитри",
        "city": "Malaysia",
        "type": "Государственный праздник",
        "note": "Крупный праздник. Возможны поездки между городами и снижение активности части водителей."
    },
    {
        "date": "2026-05-01",
        "title": "День труда",
        "city": "Malaysia",
        "type": "Государственный праздник",
        "note": "Общий выходной день."
    },
    {
        "date": "2026-05-31",
        "title": "Гавай / Gawai Dayak",
        "city": "Miri",
        "type": "Региональный праздник",
        "note": "Актуально для Sarawak."
    },
    {
        "date": "2026-05-31",
        "title": "Гавай / Gawai Dayak",
        "city": "Bintulu",
        "type": "Региональный праздник",
        "note": "Актуально для Sarawak."
    },
    {
        "date": "2026-05-31",
        "title": "Гавай / Gawai Dayak",
        "city": "Sibu",
        "type": "Региональный праздник",
        "note": "Актуально для Sarawak."
    },
    {
        "date": "2026-08-31",
        "title": "День независимости / Merdeka Day",
        "city": "Malaysia",
        "type": "Государственный праздник",
        "note": "Крупный национальный праздник."
    },
    {
        "date": "2026-09-16",
        "title": "День Малайзии / Malaysia Day",
        "city": "Malaysia",
        "type": "Государственный праздник",
        "note": "Крупный национальный праздник."
    },
    {
        "date": "2026-12-25",
        "title": "Рождество",
        "city": "Malaysia",
        "type": "Государственный праздник",
        "note": "Общий выходной день."
    },
]


LOCAL_EVENTS = [
    {
        "date": "2026-07-15",
        "title": "Локальное событие: проверить городские мероприятия",
        "city": "Miri",
        "type": "Локальное мероприятие",
        "note": "Заглушка. Позже можно заменить на реальные события из источников."
    },
    {
        "date": "2026-07-15",
        "title": "Локальное событие: проверить городские мероприятия",
        "city": "Bintulu",
        "type": "Локальное мероприятие",
        "note": "Заглушка. Позже можно заменить на реальные события из источников."
    },
    {
        "date": "2026-07-15",
        "title": "Локальное событие: проверить городские мероприятия",
        "city": "Labuan",
        "type": "Локальное мероприятие",
        "note": "Заглушка. Позже можно заменить на реальные события из источников."
    },
    {
        "date": "2026-07-15",
        "title": "Локальное событие: проверить городские мероприятия",
        "city": "Sibu",
        "type": "Локальное мероприятие",
        "note": "Заглушка. Позже можно заменить на реальные события из источников."
    },
    {
        "date": "2026-07-15",
        "title": "Локальное событие: проверить городские мероприятия",
        "city": "Seremban",
        "type": "Локальное мероприятие",
        "note": "Заглушка. Позже можно заменить на реальные события из источников."
    },
]


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def days_until(event_date: date) -> int:
    return (event_date - date.today()).days


def get_upcoming_items(days: int = LOOKAHEAD_DAYS) -> list[dict]:
    today = date.today()
    limit = today + timedelta(days=days)

    items = []

    for item in HOLIDAYS + LOCAL_EVENTS:
        event_date = parse_date(item["date"])

        if today <= event_date <= limit:
            copied = item.copy()
            copied["days_left"] = days_until(event_date)
            items.append(copied)

    items.sort(key=lambda x: x["date"])

    return items


def format_days_left(days_left: int) -> str:
    if days_left == 0:
        return "сегодня"
    if days_left == 1:
        return "завтра"
    return f"через {days_left} дн."


def format_calendar() -> str:
    items = get_upcoming_items()

    lines = [
        "📅 Праздники и мероприятия",
        "━━━━━━━━━━━━━━━━━━",
        "",
        f"Период проверки: ближайшие {LOOKAHEAD_DAYS} дней",
        ""
    ]

    if not items:
        lines.append("На ближайшие дни событий не найдено.")
        return "\n".join(lines)

    for item in items:
        lines.append(f"📍 {item['city']}")
        lines.append(f"Дата: {item['date']} ({format_days_left(item['days_left'])})")
        lines.append(f"Событие: {item['title']}")
        lines.append(f"Тип: {item['type']}")

        if item.get("note"):
            lines.append(f"Комментарий: {item['note']}")

        lines.append("")

    return "\n".join(lines)
