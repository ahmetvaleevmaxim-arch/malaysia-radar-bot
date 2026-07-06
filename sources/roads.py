from config import CITIES
from sources.google_news import fetch_google_news
from analyzers.classifier import classify_events
from analyzers.deduplicator import deduplicate_events


ROAD_QUERIES = [
    "traffic",
    "road closure",
    "accident",
    "flood",
    "landslide",
    "road works",
    "highway",
    "traffic jam",
    "police roadblock",
]


def collect_city_roads(city: str, keywords: list[str]):
    events = []

    for keyword in keywords:
        for road_query in ROAD_QUERIES:
            events.extend(
                fetch_google_news(
                    query=f"{keyword} {road_query}",
                    event_type="transport",
                    city=city,
                    max_items=10,
                )
            )

    events = deduplicate_events(events)
    events = classify_events(events)
    events.sort(key=lambda event: event.priority, reverse=True)

    return events[:8]


def collect_all_roads():
    result = {}

    for city, data in CITIES.items():
        result[city] = collect_city_roads(
            city=city,
            keywords=data.get("keywords", [city]),
        )

    return result
