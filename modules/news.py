import html
import re
from urllib.parse import quote_plus

import feedparser
import requests

from config import CITIES, NEWS_SOURCES, COMPETITORS, MAXIM_KEYWORDS


MAX_ITEMS_COUNTRY = 8
MAX_ITEMS_CITY = 5
MAX_ITEMS_COMPETITOR = 4
MAX_ITEMS_MAXIM = 6


NEGATIVE_WORDS = [
    "complaint", "bad", "rude", "scam", "angry", "problem", "late",
    "expensive", "overcharge", "dangerous", "accident", "police",
    "ban", "blocked", "issue", "viral", "negative", "fraud",
    "жалоба", "плохо", "грубо", "проблема", "обман", "дорого"
]


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


def is_negative(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in NEGATIVE_WORDS)


def google_news_rss(query: str) -> str:
    encoded = quote_plus(query)
    return (
        "https://news.google.com/rss/search?"
        f"q={encoded}"
        "&hl=en-MY&gl=MY&ceid=MY:en"
    )


def parse_feed(url: str, limit: int = 10) -> list[dict]:
    result = []

    try:
        feed = feedparser.parse(url)

        for entry in feed.entries[:limit]:
            title = clean_text(entry.get("title", ""))
            summary = clean_text(entry.get("summary", ""))
            link = entry.get("link", "")
            published = entry.get("published", "")

            if not title:
                continue

            result.append({
                "title": title,
                "summary": summary,
                "url": link,
                "published": published,
                "source": feed.feed.get("title", "Источник"),
            })

    except Exception:
        pass

    return result


def deduplicate(items: list[dict]) -> list[dict]:
    seen = set()
    result = []

    for item in items:
        key = normalize_title(item.get("title", ""))

        if not key or key in seen:
            continue

        seen.add(key)
        result.append(item)

    return result


def collect_country_news() -> list[dict]:
    items = []

    for urls in NEWS_SOURCES.values():
        for url in urls:
            items.extend(parse_feed(url, limit=15))

    items.extend(parse_feed(google_news_rss("Malaysia latest news"), limit=15))
    items.extend(parse_feed(google_news_rss("Malaysia transport e-hailing taxi"), limit=15))

    return deduplicate(items)[:MAX_ITEMS_COUNTRY]


def collect_city_news(city: str, keywords: list[str]) -> list[dict]:
    items = []

    for keyword in keywords:
        items.extend(parse_feed(google_news_rss(f"{keyword} Malaysia news"), limit=10))
        items.extend(parse_feed(google_news_rss(f"{keyword} local event"), limit=10))
        items.extend(parse_feed(google_news_rss(f"{keyword} traffic weather transport"), limit=10))

    return deduplicate(items)[:MAX_ITEMS_CITY]


def collect_competitor_news() -> dict:
    result = {}

    for company, queries in COMPETITORS.items():
        items = []

        for query in queries:
            items.extend(parse_feed(google_news_rss(query), limit=10))

        result[company] = deduplicate(items)[:MAX_ITEMS_COMPETITOR]

    return result


def collect_maxim_mentions() -> list[dict]:
    items = []

    for keyword in MAXIM_KEYWORDS:
        items.extend(parse_feed(google_news_rss(keyword), limit=10))

    items = deduplicate(items)

    for item in items:
        text = f"{item.get('title', '')} {item.get('summary', '')}"
        item["negative"] = is_negative(text)

    items.sort(key=lambda x: x.get("negative", False), reverse=True)

    return items[:MAX_ITEMS_MAXIM]


def format_item(item: dict, index: int) -> str:
    title = translate_to_ru(item.get("title", ""))
    summary = translate_to_ru(shorten(item.get("summary", "")))

    text = f"{index}. {title}\n"

    if summary:
        text += f"{summary}\n"

    if item.get("source"):
        text += f"Источник: {item['source']}\n"

    if item.get("url"):
        text += f"Ссылка: {item['url']}\n"

    return text


def format_country_news() -> str:
    items = collect_country_news()

    lines = [
        "📰 Новости по Малайзии",
        "━━━━━━━━━━━━━━",
        ""
    ]

    if not items:
        lines.append("Новости не найдены.")
        return "\n".join(lines)

    for i, item in enumerate(items, 1):
        lines.append(format_item(item, i))

    return "\n".join(lines)


def format_city_news() -> str:
    lines = [
        "📍 Новости по городам",
        "━━━━━━━━━━━━━━",
        ""
    ]

    for city, data in CITIES.items():
        lines.append(f"📍 {city}")
        lines.append("")

        items = collect_city_news(city, data.get("keywords", [city]))

        if not items:
            lines.append("Новостей не найдено.\n")
            continue

        for i, item in enumerate(items, 1):
            lines.append(format_item(item, i))

        lines.append("")

    return "\n".join(lines)


def format_competitor_news() -> str:
    data = collect_competitor_news()

    lines = [
        "🚗 Новости конкурентов",
        "━━━━━━━━━━━━━━",
        ""
    ]

    for company, items in data.items():
        lines.append(f"🚗 {company}")
        lines.append("")

        if not items:
            lines.append("Новостей не найдено.\n")
            continue

        for i, item in enumerate(items, 1):
            lines.append(format_item(item, i))

        lines.append("")

    return "\n".join(lines)


def format_maxim_mentions() -> str:
    items = collect_maxim_mentions()

    lines = [
        "🚨 Упоминания Maxim",
        "━━━━━━━━━━━━━━",
        ""
    ]

    if not items:
        lines.append("Упоминаний не найдено.")
        return "\n".join(lines)

    for i, item in enumerate(items, 1):
        status = "🔴 Возможный негатив" if item.get("negative") else "🟢 Обычное упоминание"
        lines.append(status)
        lines.append(format_item(item, i))

    return "\n".join(lines)


def format_news() -> str:
    return "\n\n".join([
        format_country_news(),
        format_city_news(),
        format_competitor_news(),
        format_maxim_mentions(),
    ])
