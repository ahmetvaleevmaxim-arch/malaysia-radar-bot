import re

from core.models import RadarEvent
from core.text import clean_text


def normalize(value: str) -> str:
    value = clean_text(value).lower()
    value = re.sub(r"[^a-zа-я0-9 ]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def deduplicate_events(events: list[RadarEvent]) -> list[RadarEvent]:
    seen = set()
    result = []

    for event in events:
        key = event.url or normalize(event.title)

        if not key:
            continue

        if key in seen:
            continue

        seen.add(key)
        result.append(event)

    return result
