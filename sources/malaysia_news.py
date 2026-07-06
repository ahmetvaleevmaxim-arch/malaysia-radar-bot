from config import NEWS_SOURCES
from sources.rss import fetch_rss
from sources.google_news import fetch_google_news
from analyzers.classifier import classify_events
from analyzers.deduplicator import deduplicate_events


def collect_malaysia_news():
    events = []

    for source_group in NEWS_SOURCES.values():
        for url in source_group:
            events.extend(
                fetch_rss(
                    url=url,
                    event_type="country_news",
                    city="Malaysia",
                    max_items=30,
                )
            )

    queries = [
        "Malaysia latest news",
        "Malaysia government",
        "Malaysia transport",
        "Malaysia economy",
        "Malaysia e-hailing",
        "Malaysia taxi",
        "Malaysia public transport",
    ]

    for query in queries:
        events.extend(
            fetch_google_news(
                query=query,
                event_type="country_news",
                city="Malaysia",
                max_items=20,
            )
        )

    events = deduplicate_events(events)
    events = classify_events(events)

    return events[:15]
