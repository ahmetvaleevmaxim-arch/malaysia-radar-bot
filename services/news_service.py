import html
import re
from urllib.parse import quote_plus

import feedparser
import requests

from config import CITIES, NEWS_SOURCES


MAX_ITEMS_COUNTRY = 8
MAX_ITEMS_CITY = 5


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = html.unescape(text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def translate_to_ru(text: str) -> str:
    if not text:
        return ""

    try:
        url = "https://translate.googleapis.com/translate_a/single"

        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "ru",
            "dt": "t",
            "q": text,
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        translated = "".join(part[0] for part in data[0] if part[0])

        return translated.strip()

    except Exception:
        return text


def shorten(text: str, limit: int = 220) -> str:
    text = clean_text(text)

    if len(text) <= limit:
        return text

    return text[:limit].rsplit(" ", 1)[0] + "..."


def normalize_title(title: str) -> str:
    title = clean_text(title).lower()
    title = re.sub(r"[^a-zа-я0-9 ]", "", title)
    title = re.sub(r"\s+", " ", title)

    return title.strip()


def google_news_rss(query: str) -> str:
    encoded = quote_plus(query)

    return (
        "https://news.google.com/rss/search?"
        f"q={encoded}"
        "&hl=en-MY&gl=MY&ceid=MY:en"
    )


def parse_feed(url: str, limit: int = 10) -> list[dict]:
    items = []

    try:
        feed = feedparser.parse(url)

        for entry in feed.entries[:limit]:
            title = clean_text(entry.get("title", ""))
            summary = clean_text(entry.get("summary", ""))
            link = entry.get("link", "")
            published = entry.get("published", "")
            source = feed.feed.get("title", "Источник")

            if not title:
                continue

            items.append({
                "title": title,
                "summary": summary,
                "url": link,
                "published": published,
                "source": source,
            })

    except Exception:
        pass

    return items


def deduplicate(items: list[dict]) -> list[dict]:
    seen = set()
    result = []

    for item in items:
        key = normalize_title(item.get("title", ""))

        if not key:
            continue

        if key in seen:
            continue

        seen.add(key)
        result.append(item)

    return result


def collect_country_news() -> list[dict]:
    items = []

    for source_group in NEWS_SOURCES.values():
        for url in source_group:
            items.extend(parse_feed(url, limit=15))

    items.extend(parse_feed(google_news_rss("Malaysia latest news"), limit=15))
    items.extend(parse_feed(google_news_rss("Malaysia transport e-hailing taxi"), limit=15))

    return deduplicate(items)[:MAX_ITEMS_COUNTRY]


def collect_city_news(city: str, keywords: list[str]) -> list[dict]:
    items = []

    for keyword in keywords:
        items.extend(parse_feed(google_news_rss(f"{keyword} Malaysia news"), limit=10))
        items.extend(parse_feed(google_news_rss(f"{keyword} local event"), limit=10))
        items.extend(parse_feed(google_news_rss(f"{keyword} traffic transport weather"), limit=10))

    return deduplicate(items)[:MAX_ITEMS_CITY]


def collect_all_city_news() -> dict:
    result = {}

    for city, data in CITIES.items():
        result[city] = collect_city_news(
            city,
            data.get("keywords", [city])
        )

    return result
