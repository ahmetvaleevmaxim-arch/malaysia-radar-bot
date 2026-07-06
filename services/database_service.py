import sqlite3

from config import DATABASE_NAME


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def save_news(news: list[dict]):

    conn = get_connection()

    cur = conn.cursor()

    for item in news:

        try:

            cur.execute(
                """
                INSERT OR IGNORE INTO news
                (
                    city,
                    title,
                    summary,
                    source,
                    url,
                    published
                )
                VALUES
                (?, ?, ?, ?, ?, ?)
                """,
                (
                    item.get("city", "Malaysia"),
                    item.get("title"),
                    item.get("summary"),
                    item.get("source"),
                    item.get("url"),
                    item.get("published"),
                ),
            )

        except Exception:
            pass

    conn.commit()

    conn.close()


def save_competitor_news(company, news):

    conn = get_connection()

    cur = conn.cursor()

    for item in news:

        try:

            cur.execute(
                """
                INSERT OR IGNORE INTO competitors
                (
                    company,
                    title,
                    summary,
                    url
                )
                VALUES
                (?, ?, ?, ?)
                """,
                (
                    company,
                    item.get("title"),
                    item.get("summary"),
                    item.get("url"),
                ),
            )

        except Exception:
            pass

    conn.commit()

    conn.close()


def save_maxim_mentions(items):

    conn = get_connection()

    cur = conn.cursor()

    for item in items:

        try:

            cur.execute(
                """
                INSERT OR IGNORE INTO maxim_monitor
                (
                    platform,
                    city,
                    category,
                    author,
                    text,
                    url,
                    priority
                )
                VALUES
                (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "Google News",
                    item.get("city"),
                    item.get("category"),
                    "",
                    item.get("title"),
                    item.get("url"),
                    item.get("priority"),
                ),
            )

        except Exception:
            pass

    conn.commit()

    conn.close()


def save_currency(rates):

    if rates is None:
        return

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO currency
        (
            usd,
            eur,
            rub,
            cny
        )
        VALUES
        (?, ?, ?, ?)
        """,
        (
            rates["USD"],
            rates["EUR"],
            rates["RUB"],
            rates["CNY"],
        ),
    )

    conn.commit()

    conn.close()


def save_weather(city, weather):

    if weather is None:
        return

    current = weather["current"]

    hourly = weather["hourly"]

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO weather
        (
            city,
            temperature,
            weather,
            humidity,
            wind,
            rain,
            forecast_1h,
            forecast_2h,
            forecast_3h
        )
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            city,
            current["temperature_2m"],
            str(current["weather_code"]),
            current["relative_humidity_2m"],
            current["wind_speed_10m"],
            0,
            str(hourly["weather_code"][0]),
            str(hourly["weather_code"][1]),
            str(hourly["weather_code"][2]),
        ),
    )

    conn.commit()

    conn.close()
