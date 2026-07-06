from services.news_service import collect_country_news, collect_all_city_news
from services.weather_service import get_all_weather
from services.currency_service import get_currency_rates
from services.competitor_service import get_all_competitors
from services.maxim_service import get_maxim_mentions
from services.database_service import (
    save_news,
    save_weather,
    save_currency,
    save_competitor_news,
    save_maxim_mentions,
)


def collect_news_job():
    country_news = collect_country_news()

    for item in country_news:
        item["city"] = "Malaysia"

    save_news(country_news)

    city_news = collect_all_city_news()

    for city, items in city_news.items():
        for item in items:
            item["city"] = city

        save_news(items)


def collect_weather_job():
    weather = get_all_weather()

    for city, data in weather.items():
        save_weather(city, data)


def collect_currency_job():
    rates = get_currency_rates()
    save_currency(rates)


def collect_competitors_job():
    data = get_all_competitors()

    for company, items in data.items():
        save_competitor_news(company, items)


def collect_maxim_job() -> list[dict]:
    mentions = get_maxim_mentions()
    save_maxim_mentions(mentions)

    important = []

    for item in mentions:
        if item.get("priority", 0) >= 4:
            important.append(item)

    return important


def collect_all_job() -> list[dict]:
    collect_news_job()
    collect_weather_job()
    collect_currency_job()
    collect_competitors_job()
    important_mentions = collect_maxim_job()

    return important_mentions
