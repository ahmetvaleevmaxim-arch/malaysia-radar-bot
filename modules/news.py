import feedparser
from config import CITIES, NEWS_SOURCES
from modules.utils import trim


def _read_feed(url: str, limit: int = 20):
    feed = feedparser.parse(url)
    items = []

    for entry in feed.entries[:limit]:
        title = trim(entry.get("title", ""), 180)
        summary = trim(entry.get("summary", ""), 250)
        link = entry.get("link", "")
        published = entry.get("published", "")

        if title:
            items.append({
                "title": title,
                "summary": summary,
                "link": link,
                "published": published,
            })

    return items


def collect_news():
    raw_items = []

    for source_group, urls in NEWS_SOURCES.items():
        for url in urls:
            try:
                for item in _read_feed(url):
                    item["source_group"] = source_group
                    raw_items.append(item)
            except Exception:
                continue

    result = {"Malaysia": raw_items[:8]}

    for city, info in CITIES.items():
        keywords = [k.lower() for k in info["keywords"]]
        city_items = []

        for item in raw_items:
            text = f"{item.get('title', '')} {item.get('summary', '')}".lower()
            if any(keyword in text for keyword in keywords):
                city_items.append(item)

        result[city] = city_items[:5]

    return result


def format_news():
    data = collect_news()
    lines = ["📰 Новости Малайзии\n"]

    malaysia = data.get("Malaysia", [])
    lines.append("🇲🇾 Общие новости:")
    if not malaysia:
        lines.append("Новостей не найдено.")
    else:
        for index, item in enumerate(malaysia[:5], start=1):
            lines.append(f"{index}. {item['title']}\n{item['link']}")

    for city in CITIES:
        lines.append(f"\n📍 {city}:")
        items = data.get(city, [])
        if not items:
            lines.append("Локальных новостей не найдено.")
        else:
            for index, item in enumerate(items[:3], start=1):
                lines.append(f"{index}. {item['title']}\n{item['link']}")

    return "\n".join(lines)
