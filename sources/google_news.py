from urllib.parse import quote_plus

import feedparser

from core.models import RadarEvent
from core.text import clean_text
from core.time import is_today_myt


def google_news_url(query: str) -> str:
    return (
        "https://news.google.com/rss/search?"
        f"q={quote_plus(query + ' when:1d')}"
        "&hl=en-MY&gl=MY&ceid=MY:en"
    )


def fetch_google_news(
    query: str,
    event_type: str,
    city: str = "Malaysia",
    company: str | None = None,
    max_items: int = 10,
) -> list[RadarEvent]:
    url = google_news_url(query)
    feed = feedparser.parse(url)

    events = []

    for entry in feed.entries[:max_items]:
        published = entry.get("published") or entry.get("updated") or ""

        if not is_today_myt(published):
            continue

        title = clean_text(entry.get("title", ""))
        summary = clean_text(entry.get("summary", ""))
        link = entry.get("link", "")

        if not title or not link:
            continue

        events.append(
            RadarEvent(
                event_type=event_type,
                title=title,
                summary=summary,
                city=city,
                company=company,
                source="Google News",
                url=link,
                priority=1,
            )
        )

    return eventsfrom urllib.parse import quote_plus

import feedparser

from core.models import RadarEvent
from core.text import clean_text
from core.time import is_today_myt


def google_news_url(query: str) -> str:
    return (
        "https://news.google.com/rss/search?"
        f"q={quote_plus(query + ' when:1d')}"
        "&hl=en-MY&gl=MY&ceid=MY:en"
    )


def fetch_google_news(
    query: str,
    event_type: str,
    city: str = "Malaysia",
    company: str | None = None,
    max_items: int = 10,
) -> list[RadarEvent]:
    url = google_news_url(query)
    feed = feedparser.parse(url)

    events = []

    for entry in feed.entries[:max_items]:
        published = entry.get("published") or entry.get("updated") or ""

        if not is_today_myt(published):
            continue

        title = clean_text(entry.get("title", ""))
        summary = clean_text(entry.get("summary", ""))
        link = entry.get("link", "")

        if not title or not link:
            continue

        events.append(
            RadarEvent(
                event_type=event_type,
                title=title,
                summary=summary,
                city=city,
                company=company,
                source="Google News",
                url=link,
                priority=1,
            )
        )

    return events
