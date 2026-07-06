import requests


API_URL = "https://open.er-api.com/v6/latest/MYR"


def get_currency_rates() -> dict | None:
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
