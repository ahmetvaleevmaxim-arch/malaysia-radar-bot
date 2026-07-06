from sources.malaysia_news import collect_malaysia_news
from sources.city_news import collect_all_city_news
from sources.competitors import collect_all_competitors
from sources.maxim_monitor import collect_maxim_mentions
from sources.weather import collect_weather_events
from sources.currency import collect_currency_events
from sources.government import collect_government_events
from sources.roads import collect_all_roads
from analyzers.deduplicator import deduplicate_events


def collect_all_events():
    events = []

    events.extend(collect_malaysia_news())

    city_news = collect_all_city_news()
    for items in city_news.values():
        events.extend(items)

    competitors = collect_all_competitors()
    for items in competitors.values():
        events.extend(items)

    events.extend(collect_maxim_mentions())
    events.extend(collect_government_events())

    roads = collect_all_roads()
    for items in roads.values():
        events.extend(items)

    events.extend(collect_weather_events())
    events.extend(collect_currency_events())

    events = deduplicate_events(events)
    events.sort(key=lambda event: event.priority, reverse=True)

    return events
