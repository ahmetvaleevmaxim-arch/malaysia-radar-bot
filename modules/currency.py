import requests


def collect_currency():
    # Free public endpoint, no API key.
    url = "https://open.er-api.com/v6/latest/MYR"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    data = response.json()

    rates = data.get("rates", {})
    return {
        "MYR_USD": rates.get("USD"),
        "MYR_RUB": rates.get("RUB"),
        "MYR_EUR": rates.get("EUR"),
        "MYR_SGD": rates.get("SGD"),
        "updated": data.get("time_last_update_utc"),
    }


def format_currency():
    try:
        data = collect_currency()
        return (
            "💱 Курсы валют от MYR\n\n"
            f"1 MYR = {data.get('MYR_USD')} USD\n"
            f"1 MYR = {data.get('MYR_RUB')} RUB\n"
            f"1 MYR = {data.get('MYR_EUR')} EUR\n"
            f"1 MYR = {data.get('MYR_SGD')} SGD\n\n"
            f"Обновлено: {data.get('updated')}"
        )
    except Exception as exc:
        return f"💱 Курсы валют\n\nОшибка получения данных: {exc}"
