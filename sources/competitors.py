from config import COMPETITORS
from sources.google_news import fetch_google_news
from analyzers.classifier import classify_events
from analyzers.deduplicator import deduplicate_events


def collect_competitor_news(company: str, queries: list[str]):
    events = []

    expanded_queries = []

    for query in queries:
        expanded_queries.extend([
            query,
            f"{query} Malaysia",
            f"{query} promotion",
            f"{query} promo",
            f"{query} driver",
            f"{query} commission",
            f"{query} fare",
            f"{query} e-hailing",
        ])

    for query in expanded_queries:
        events.extend(
            fetch_google_news(
                query=query,
                event_type="competitor",
                city="Malaysia",
                company=company,
                max_items=10,
            )
        )

    events = deduplicate_events(events)
    events = classify_events(events)

    return events[:8]


def collect_all_competitors():
    result = {}

    for company, queries in COMPETITORS.items():
        result[company] = collect_competitor_news(company, queries)

    return result
