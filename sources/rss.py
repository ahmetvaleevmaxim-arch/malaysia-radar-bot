import feedparser

from core.models import RadarEvent
from core.text import clean_text
from core.time import is_today_myt


def fetch_rss(
    url: str,
    event_type: str,
    city: str = "Malaysia",
    source_name: str = "",
    max_items: int = 20,
) -> list[RadarEvent]:
    feed = feedparser.parse(url)

    events = []
    source = source_name or feed.feed.get("title", "RSS")

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
                source=source,
                url=link,
                priority=1,
            )
        )

    return events
