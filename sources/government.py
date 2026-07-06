from sources.google_news import fetch_google_news
from analyzers.classifier import classify_events
from analyzers.deduplicator import deduplicate_events


GOVERNMENT_QUERIES = {
    "APAD": [
        "APAD Malaysia e-hailing",
        "APAD Malaysia taxi",
        "APAD Malaysia PSV",
        "APAD Malaysia EVP",
        "Agensi Pengangkutan Awam Darat e-hailing",
    ],
    "JPJ": [
        "JPJ Malaysia e-hailing",
        "JPJ Malaysia road transport",
        "JPJ Malaysia driver license",
        "JPJ Malaysia vehicle inspection",
    ],
    "MOT": [
        "Ministry of Transport Malaysia e-hailing",
        "MOT Malaysia public transport",
        "MOT Malaysia taxi",
        "Anthony Loke e-hailing",
    ],
    "LPKP": [
        "LPKP Sabah e-hailing",
        "LPKP Sarawak e-hailing",
        "Lembaga Pelesenan Kenderaan Perdagangan Sabah",
        "Lembaga Pelesenan Kenderaan Perdagangan Sarawak",
    ],
    "PUSPAKOM": [
        "PUSPAKOM Malaysia inspection",
        "PUSPAKOM e-hailing",
        "PUSPAKOM taxi",
    ],
}


def collect_government_events():
    events = []

    for agency, queries in GOVERNMENT_QUERIES.items():
        for query in queries:
            events.extend(
                fetch_google_news(
                    query=query,
                    event_type="government",
                    city="Malaysia",
                    company=agency,
                    max_items=10,
                )
            )

    events = deduplicate_events(events)
    events = classify_events(events)
    events.sort(key=lambda event: event.priority, reverse=True)

    return events[:15]
