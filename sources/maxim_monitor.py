from sources.google_news import fetch_google_news
from analyzers.classifier import classify_events
from analyzers.deduplicator import deduplicate_events


MAXIM_QUERIES = [
    '"Maxim Malaysia" e-hailing',
    '"Maxim Malaysia" taxi',
    '"Maxim Malaysia" driver',
    '"Maxim e-hailing" Malaysia',
    '"Maxim taxi" Malaysia',
    '"Maxim driver" Malaysia',
    '"Maxim Miri"',
    '"Maxim Bintulu"',
    '"Maxim Labuan"',
    '"Maxim Sibu"',
    '"Maxim Seremban"',
    'site:facebook.com "Maxim" "Malaysia" "e-hailing"',
    'site:facebook.com "Maxim" "Miri"',
    'site:facebook.com "Maxim" "Bintulu"',
    'site:facebook.com "Maxim" "Labuan"',
    'site:facebook.com "Maxim" "Sibu"',
    'site:facebook.com "Maxim" "Seremban"',
    'site:tiktok.com "Maxim" "Malaysia" "e-hailing"',
    'site:instagram.com "Maxim" "Malaysia" "e-hailing"',
    'site:reddit.com "Maxim" "Malaysia" "e-hailing"',
    'site:x.com "Maxim" "Malaysia" "e-hailing"',
    'site:youtube.com "Maxim" "Malaysia" "e-hailing"',
]

EXCLUDE_WORDS = [
    "maximilian",
    "maxim gorky",
    "maxim magazine",
    "maxim group",
    "maxim integrated",
    "maxim healthcare",
    "maxim coffee",
]


def is_relevant_maxim(event) -> bool:
    text = f"{event.title} {event.summary}".lower()

    if "maxim" not in text:
        return False

    if any(word in text for word in EXCLUDE_WORDS):
        return False

    context_words = [
        "malaysia",
        "e-hailing",
        "ehailing",
        "taxi",
        "ride",
        "driver",
        "miri",
        "bintulu",
        "labuan",
        "sibu",
        "seremban",
    ]

    return any(word in text for word in context_words)


def detect_city(event):
    text = f"{event.title} {event.summary}".lower()

    for city in ["Miri", "Bintulu", "Labuan", "Sibu", "Seremban"]:
        if city.lower() in text:
            event.city = city
            return event

    event.city = "Malaysia"
    return event


def collect_maxim_mentions():
    events = []

    for query in MAXIM_QUERIES:
        events.extend(
            fetch_google_news(
                query=query,
                event_type="maxim",
                city="Malaysia",
                company="Maxim",
                max_items=10,
            )
        )

    events = [event for event in events if is_relevant_maxim(event)]
    events = [detect_city(event) for event in events]
    events = deduplicate_events(events)
    events = classify_events(events)

    events.sort(key=lambda event: event.priority, reverse=True)

    return events[:12]
