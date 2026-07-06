from core.models import RadarEvent


CRITICAL_WORDS = [
    "apad", "lpkp", "jpj", "police", "accident", "viral",
    "ban", "blocked", "lawsuit", "sue", "strike", "flood",
    "landslide", "road closure",
]

IMPORTANT_WORDS = [
    "grab", "indrive", "bolt", "airasia ride", "myride",
    "e-hailing", "ehailing", "taxi", "driver", "fare",
    "commission", "promotion", "promo", "festival", "concert",
    "event", "airport", "ferry", "traffic", "rain", "thunderstorm",
]

NEGATIVE_WORDS = [
    "complaint", "complain", "bad", "rude", "scam", "angry",
    "problem", "late", "expensive", "overcharge", "dangerous",
    "fraud", "fake", "refund", "cancel", "delay", "terrible",
    "worst", "cheat", "damage",
]


def classify_event(event: RadarEvent) -> RadarEvent:
    text = f"{event.title} {event.summary}".lower()

    if any(word in text for word in CRITICAL_WORDS):
        event.priority = max(event.priority, 5)
    elif any(word in text for word in IMPORTANT_WORDS):
        event.priority = max(event.priority, 4)
    else:
        event.priority = max(event.priority, 2)

    if event.event_type == "maxim":
        if any(word in text for word in NEGATIVE_WORDS):
            event.category = "негатив"
            event.priority = max(event.priority, 4)
        else:
            event.category = "упоминание"

    return event


def classify_events(events: list[RadarEvent]) -> list[RadarEvent]:
    return [classify_event(event) for event in events]
