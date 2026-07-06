import requests

from core.models import RadarEvent


API_URL = "https://open.er-api.com/v6/latest/MYR"


def fetch_currency_rates() -> dict | None:
    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()
        data = response.json()

        rates = data.get("rates", {})

        return {
            "USD": round(1 / rates["USD"], 4),
            "EUR": round(1 / rates["EUR"], 4),
            "RUB": round(1 / rates["RUB"], 4),
            "CNY": round(1 / rates["CNY"], 4),
        }

    except Exception:
        return None


def collect_currency_events() -> list[RadarEvent]:
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
        f"USD → MYR: {rates['USD']}\n"
        f"EUR → MYR: {rates['EUR']}\n"
        f"RUB → MYR: {rates['RUB']}\n"
        f"CNY → MYR: {rates['CNY']}"
    )

    return [
        RadarEvent(
            event_type="currency",
            title="Курсы валют",
            summary=summary,
            source="ExchangeRate API",
            priority=1,
        )
    ]
