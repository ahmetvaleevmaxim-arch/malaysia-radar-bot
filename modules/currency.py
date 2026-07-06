from services.currency_service import get_currency_rates


def format_currency() -> str:
    rates = get_currency_rates()

    lines = [
        "💰 Курсы валют",
        "━━━━━━━━━━━━━━━━━━",
        ""
    ]

    if rates is None:
        lines.append("Не удалось получить курсы валют.")
        return "\n".join(lines)

    lines.append(f"🇺🇸 USD → MYR: {rates['USD']}")
    lines.append(f"🇪🇺 EUR → MYR: {rates['EUR']}")
    lines.append(f"🇷🇺 RUB → MYR: {rates['RUB']}")
    lines.append(f"🇨🇳 CNY → MYR: {rates['CNY']}")
    lines.append("")
    lines.append("Источник: ExchangeRate API")

    return "\n".join(lines)
