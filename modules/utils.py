from datetime import datetime
from zoneinfo import ZoneInfo

MYT = ZoneInfo("Asia/Kuala_Lumpur")


def now_myt() -> datetime:
    return datetime.now(MYT)


def safe(value, fallback="нет данных"):
    if value is None or value == "":
        return fallback
    return value


def trim(text: str, max_len: int = 300) -> str:
    text = " ".join((text or "").split())
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"
