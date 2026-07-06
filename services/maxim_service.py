from urllib.parse import quote_plus

import feedparser

from config import CITIES


MAX_ITEMS = 10

MAXIM_QUERIES = [
    '"Maxim Malaysia"',
    '"Maxim e-hailing" Malaysia',
    '"Maxim ride" Malaysia',
    '"Maxim taxi" Malaysia',
    '"Maxim driver" Malaysia',
    '"Maxim app" Malaysia',
    '"Maxim Miri"',
    '"Maxim Bintulu"',
    '"Maxim Labuan"',
    '"Maxim Sibu"',
    '"Maxim Seremban"',
    '"Maxim" "e-hailing" "Malaysia"',
    '"Maxim" "driver" "Malaysia"',
    '"Maxim" "taxi" "Malaysia"',
]

SOCIAL_QUERIES = [
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
]

NEGATIVE_WORDS = [
    "complaint",
    "complain",
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
    "terrible",
    "worst",
    "cheat",
    "cheated",
    "report",
    "sue",
    "damage",
    "driver",
    "customer service",
]

EXCLUDE_WORDS = [
    "maximilian",
    "maxim gorky",
    "maxim magazine",
    "maxim group",
    "maxim integrated",
    "maxim healthcare",
    "maxim coffee",
    "maximilian",
]


def google_news(query: str) -> str:
    return (
        "https://news.google.com/rss/search?"
        f"q={quote_plus(query + ' when:1d')}"
        "&hl=en-MY"
        "&gl=MY"
        "&ceid=MY:en"
    )


def is_relevant_maxim(text: str) -> bool:
    low = text.lower()

    if any(word in low for word in EXCLUDE_WORDS):
        return False

    must_have_context = [
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

    if "maxim" not in low:
        return False

    return any(word in low for word in must_have_context)


def detect_city(text: str) -> str:
    low = text.lower()

    for city, data in CITIES.items():
        keywords = data.get("keywords", [city])

        for keyword in keywords:
            if keyword.lower() in low:
                return city

    return "Malaysia"


def detect_category(text: str) -> str:
    low = text.lower()

    if any(word in low for word in NEGATIVE_WORDS):
        return "негатив"

    return "упоминание"


def detect_priority(text: str) -> int:
    low = text.lower()

    if "viral" in low or "police" in low or "accident" in low or "sue" in low:
        return 5

    if any(word in low for word in NEGATIVE_WORDS):
        return 4

    return 2


def parse_feed(url: str) -> list[dict]:
    feed = feedparser.parse(url)
    items = []

    for item in feed.entries[:MAX_ITEMS]:
        title = item.get("title", "")
        summary = item.get("summary", "")
        link = item.get("link", "")
        published = item.get("published", "")

        text = f"{title} {summary}"

        if not is_relevant_maxim(text):
            continue

        items.append({
            "title": title,
            "summary": summary,
            "url": link,
            "published": published,
            "city": detect_city(text),
            "category": detect_category(text),
            "priority": detect_priority(text),
        })

    return items


def get_maxim_mentions() -> list[dict]:
    result = []

    for query in MAXIM_QUERIES + SOCIAL_QUERIES:
        try:
            result.extend(parse_feed(google_news(query)))
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
