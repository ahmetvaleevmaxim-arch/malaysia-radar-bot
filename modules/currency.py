import requests


API = "https://open.er-api.com/v6/latest/MYR"


def get_rates():

    try:

        response = requests.get(API, timeout=15)

        response.raise_for_status()

        data = response.json()

        rates = data["rates"]

        return {

            "USD": round(1 / rates["USD"], 4),

            "EUR": round(1 / rates["EUR"], 4),

            "RUB": round(1 / rates["RUB"], 4),

            "CNY": round(1 / rates["CNY"], 4),

        }

    except Exception:

        return None


def format_currency():

    rates = get_rates()

    report = []

    report.append("💰 Курсы валют")

    report.append("━━━━━━━━━━━━━━━━━━")

    report.append("")

    if rates is None:

        report.append("Не удалось получить курсы валют.")

        return "\n".join(report)

    report.append(f"🇺🇸 USD → MYR : {rates['USD']}")

    report.append(f"🇪🇺 EUR → MYR : {rates['EUR']}")

    report.append(f"🇷🇺 RUB → MYR : {rates['RUB']}")

    report.append(f"🇨🇳 CNY → MYR : {rates['CNY']}")

    report.append("")

    report.append("Источник: ExchangeRate API")

    return "\n".join(report)
