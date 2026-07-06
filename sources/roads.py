from config import CITIES
from sources.google_news import fetch_google_news
from analyzers.classifier import classify_events
from analyzers.deduplicator import deduplicate_events


MAX_ITEMS_PER_CITY = 8


ROAD_QUERY_TERMS = [
    "accident",
    "crash",
    "fatal accident",
    "road closure",
    "road closed",
    "traffic jam",
    "traffic congestion",
    "police roadblock",
    "flood",
    "flash flood",
    "landslide",
    "sinkhole",
    "bridge closed",
    "highway closed",
    "road works",
    "traffic disruption",
]


ROAD_REQUIRED_WORDS = [
    "traffic",
    "accident",
    "crash",
    "road",
    "highway",
    "closure",
    "closed",
    "blocked",
    "roadblock",
    "flood",
    "landslide",
    "sinkhole",
    "bridge",
    "jam",
    "congestion",
    "collision",
    "fatal",
    "police",
    "lorry",
    "car",
    "motorcycle",
]


BLOCK_WORDS = [
    "property",
    "edgeprop",
    "for sale",
    "for rent",
    "shoplot",
    "shop lot",
    "house",
    "apartment",
    "condominium",
    "office",
    "warehouse",
    "auction",
    "real estate",
    "room for rent",
    "land for sale",
    "homes",
    "rental",
    "estate",
    "israel",
    "india",
    "mumbai",
    "pune",
    "sharon",
    "nantes",
    "australia",
    "canada",
    "uk",
    "united states",
]


def is_relevant_road_event(event, city: str) -> bool:
    text = f"{event.title} {event.summary}".lower()
    city_low = city.lower()

    if city_low not in text:
        return False

    if any(word in text for word in BLOCK_WORDS):
        return False

    if not any(word in text for word in ROAD_REQUIRED_WORDS):
        return False

    return True


def improve_road_priority(event):
    text = f"{event.title} {event.summary}".lower()

    critical_words = [
        "fatal",
        "death",
        "killed",
        "died",
        "serious accident",
        "road closed",
        "highway closed",
        "flash flood",
        "landslide",
        "sinkhole",
    ]

    important_words = [
        "accident",
        "crash",
        "collision",
        "road closure",
        "traffic jam",
        "congestion",
        "roadblock",
        "flood",
        "blocked",
    ]

    if any(word in text for word in critical_words):
        event.priority = max(event.priority, 5)
    elif any(word in text for word in important_words):
        event.priority = max(event.priority, 4)
    else:
        event.priority = max(event.priority, 2)

    return event


def collect_city_roads(city: str, keywords: list[str]):
    events = []

    for keyword in keywords:
        for road_term in ROAD_QUERY_TERMS:
            query = f'"{keyword}" "{road_term}" Malaysia'

            events.extend(
                fetch_google_news(
                    query=query,
                    event_type="transport",
                    city=city,
                    max_items=8,
                )
            )

    events = [
        event for event in events
        if is_relevant_road_event(event, city)
    ]

    events = deduplicate_events(events)
    events = classify_events(events)
    events = [improve_road_priority(event) for event in events]

    events.sort(key=lambda event: event.priority, reverse=True)

    return events[:MAX_ITEMS_PER_CITY]


def collect_all_roads():
    result = {}

    for city, data in CITIES.items():
        result[city] = collect_city_roads(
            city=city,
            keywords=data.get("keywords", [city]),
        )

    return result
