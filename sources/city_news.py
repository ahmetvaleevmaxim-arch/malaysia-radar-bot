from config import CITIES
from sources.google_news import fetch_google_news
from analyzers.classifier import classify_events
from analyzers.deduplicator import deduplicate_events


def collect_city_news(city: str, keywords: list[str]):
    events = []

    for keyword in keywords:
        queries = [
            f"{keyword} Malaysia news",
            f"{keyword} local news",
            f"{keyword} traffic",
            f"{keyword} weather",
            f"{keyword} event",
            f"{keyword} festival",
            f"{keyword} airport",
            f"{keyword} ferry",
            f"{keyword} police",
            f"{keyword} accident",
        ]

        for query in queries:
            events.extend(
                fetch_google_news(
                    query=query,
                    event_type="city_news",
                    city=city,
                    max_items=10,
                )
            )

    events = deduplicate_events(events)
    events = classify_events(events)

    return events[:8]


def collect_all_city_news():
    result = {}

    for city, data in CITIES.items():
        result[city] = collect_city_news(
            city=city,
            keywords=data.get("keywords", [city]),
        )

    return result
