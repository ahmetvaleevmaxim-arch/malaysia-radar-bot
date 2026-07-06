from datetime import datetime
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus
from zoneinfo import ZoneInfo

import feedparser

from config import COMPETITORS


MAX_ITEMS = 6
MY_TIMEZONE = ZoneInfo("Asia/Kuala_Lumpur")


def malaysia_today():
    return datetime.now(MY_TIMEZONE).date()


def google_news(query: str) -> str:
    return (
        "https://news.google.com/rss/search?"
        f"q={quote_plus(query + ' when:1d')}"
        "&hl=en-MY"
        "&gl=MY"
        "&ceid=MY:en"
    )


def parse_entry_date(entry) -> datetime | None:
    raw = entry.get("published") or entry.get("updated") or ""

    if not raw:
        return None

    try:
        dt = parsedate_to_datetime(raw)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=MY_TIMEZONE)

        return dt.astimezone(MY_TIMEZONE)

    except Exception:
        return None


def is_today_entry(entry) -> bool:
    dt = parse_entry_date(entry)

    if dt is None:
        return False

    return dt.date() == malaysia_today()


def parse_feed(url: str) -> list[dict]:
    feed = feedparser.parse(url)
    news = []

    for item in feed.entries[:MAX_ITEMS]:
        if not is_today_entry(item):
            continue

        title = item.get("title", "")
        link = item.get("link", "")

        if not title or not link:
            continue

        news.append({
            "title": title,
            "summary": item.get("summary", ""),
            "url": link,
            "published": item.get("published", "") or item.get("updated", ""),
            "source": "Google News",
        })

    return news


def deduplicate(items: list[dict]) -> list[dict]:
    seen = set()
    result = []

    for item in items:
        url = item.get("url")
        title = item.get("title", "").lower().strip()

        key = url or title

        if not key or key in seen:
            continue

        seen.add(key)
        result.append(item)

    return result


def get_company_news(company: str):
    result = []

    for query in COMPETITORS[company]:
        try:
            result.extend(parse_feed(google_news(query)))
        except Exception:
            pass

    return deduplicate(result)[:MAX_ITEMS]


def get_all_competitors():
    result = {}

    for company in COMPETITORS:
        result[company] = get_company_news(company)

    return result
