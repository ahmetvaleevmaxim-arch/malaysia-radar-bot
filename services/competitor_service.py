from urllib.parse import quote_plus

import feedparser

from config import COMPETITORS


MAX_ITEMS = 5


def google_news(query: str) -> str:
    return (
        "https://news.google.com/rss/search?"
        f"q={quote_plus(query)}"
        "&hl=en-MY"
        "&gl=MY"
        "&ceid=MY:en"
    )


def parse_feed(url: str):

    feed = feedparser.parse(url)

    news = []

    for item in feed.entries[:MAX_ITEMS]:

        news.append({

            "title": item.get("title", ""),

            "summary": item.get("summary", ""),

            "url": item.get("link", ""),

            "published": item.get("published", "")

        })

    return news


def get_company_news(company: str):

    result = []

    for query in COMPETITORS[company]:

        try:

            result.extend(

                parse_feed(

                    google_news(query)

                )

            )

        except Exception:

            pass

    return result


def get_all_competitors():

    result = {}

    for company in COMPETITORS:

        result[company] = get_company_news(company)

    return result
