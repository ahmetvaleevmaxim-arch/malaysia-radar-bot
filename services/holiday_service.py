from datetime import datetime, timedelta

from modules.calendar_events import HOLIDAYS, LOCAL_EVENTS


LOOK_AHEAD_DAYS = 30


def upcoming_holidays():

    today = datetime.now().date()

    limit = today + timedelta(days=LOOK_AHEAD_DAYS)

    result = []

    for holiday in HOLIDAYS:

        holiday_date = datetime.strptime(
            holiday["date"],
            "%Y-%m-%d"
        ).date()

        if today <= holiday_date <= limit:

            item = holiday.copy()

            item["days_left"] = (holiday_date - today).days

            result.append(item)

    result.sort(key=lambda x: x["date"])

    return result


def upcoming_events():

    today = datetime.now().date()

    limit = today + timedelta(days=LOOK_AHEAD_DAYS)

    result = []

    for event in LOCAL_EVENTS:

        event_date = datetime.strptime(
            event["date"],
            "%Y-%m-%d"
        ).date()

        if today <= event_date <= limit:

            item = event.copy()

            item["days_left"] = (event_date - today).days

            result.append(item)

    result.sort(key=lambda x: x["date"])

    return result


def get_calendar():

    return {

        "holidays": upcoming_holidays(),

        "events": upcoming_events()

    }
