from datetime import datetime
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo


MY_TIMEZONE = ZoneInfo("Asia/Kuala_Lumpur")


def now_myt() -> datetime:
    return datetime.now(MY_TIMEZONE)


def today_myt():
    return now_myt().date()


def parse_feed_datetime(value: str) -> datetime | None:
    if not value:
        return None

    try:
        dt = parsedate_to_datetime(value)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=MY_TIMEZONE)

        return dt.astimezone(MY_TIMEZONE)

    except Exception:
        return None


def is_today_myt(value: str) -> bool:
    dt = parse_feed_datetime(value)

    if dt is None:
        return False

    return dt.date() == today_myt()


def format_myt(dt: datetime | None = None) -> str:
    dt = dt or now_myt()
    return dt.strftime("%d.%m.%Y %H:%M MYT")
