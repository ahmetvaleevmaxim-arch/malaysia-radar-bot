from urllib.parse import quote_plus

import feedparser

from config import MAXIM_KEYWORDS, CITIES


MAX_ITEMS = 10

NEGATIVE_WORDS = [
    "complaint",
    "bad",
    "rude",
    "scam",
    "angry",
    "problem",
    "late",
    "expensive",
    "overcharge",
    "dangerous",
    "accident",
    "police",
    "ban",
    "blocked",
    "issue",
    "viral",
    "fraud",
    "fake",
    "refund",
    "cancel",
    "delay",
    "driver",
    "customer service",
]


def google_news(query: str) -> str:
    return (
        "https://news.google.com/rss/search?"
        f"q={quote_plus(query)}"
        "&hl=en-MY"
        "&gl=MY"
        "&ceid=MY:en"
    )


def parse_feed(url: str) -> list[dict]:
    feed = feedparser.parse(url)
    items = []

    for item in feed.entries[:MAX_ITEMS]:
        title = item.get("title", "")
        summary = item.get("summary", "")
        text = f"{title} {summary}".lower()

        items.append({
            "title": title,
            "summary": summary,
            "url": item.get("link", ""),
            "published": item.get("published", ""),
            "city": detect_city(text),
            "category": detect_category(text),
            "priority": detect_priority(text),
        })

    return items


def detect_city(text: str) -> str:
    for city, data in CITIES.items():
        keywords = data.get("keywords", [city])

        for keyword in keywords:
            if keyword.lower() in text:
                return city

    return "Malaysia"


def detect_category(text: str) -> str:
    if any(word in text for word in NEGATIVE_WORDS):
        return "негатив"

    return "упоминание"


def detect_priority(text: str) -> int:
    if "viral" in text or "police" in text or "accident" in text:
        return 5

    if any(word in text for word in NEGATIVE_WORDS):
        return 4

    return 2


def get_maxim_mentions() -> list[dict]:
    result = []

    for keyword in MAXIM_KEYWORDS:
        try:
            result.extend(parse_feed(google_news(keyword)))
        except Exception:
            pass

    seen = set()
    unique = []

    for item in result:
        url = item.get("url")

        if not url or url in seen:
            continue

        seen.add(url)
        unique.append(item)

    unique.sort(key=lambda x: x.get("priority", 0), reverse=True)

    return unique[:MAX_ITEMS]
