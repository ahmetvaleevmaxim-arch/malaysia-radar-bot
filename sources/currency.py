import requests

from core.models import RadarEvent


API_URL = "https://open.er-api.com/v6/latest/MYR"


def fetch_currency_rates():
    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()

        data = response.json()
        rates = data.get("rates", {})

        return {
            "USD": round(rates["USD"], 4),
            "EUR": round(rates["EUR"], 4),
            "RUB": round(rates["RUB"], 2),
            "CNY": round(rates["CNY"], 4),
            "SGD": round(rates["SGD"], 4),
        }

    except Exception:
        return None


def collect_currency_events():
    rates = fetch_currency_rates()

    if rates is None:
        return [
            RadarEvent(
                event_type="currency",
                title="Курсы валют",
                summary="Не удалось получить курсы валют.",
                source="ExchangeRate API",
                priority=1,
            )
        ]

    summary = (
        "1 MYR =\n\n"
        f"🇺🇸 {rates['USD']} USD\n"
        f"🇪🇺 {rates['EUR']} EUR\n"
        f"🇷🇺 {rates['RUB']} RUB\n"
        f"🇨🇳 {rates['CNY']} CNY\n"
        f"🇸🇬 {rates['SGD']} SGD"
    )

    return [
        RadarEvent(
            event_type="currency",
            title="Стоимость 1 MYR",
            summary=summary,
            source="ExchangeRate API",
            priority=1,
        )
    ]
