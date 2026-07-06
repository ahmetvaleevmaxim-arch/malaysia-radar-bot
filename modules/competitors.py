from modules.news import collect_competitor_news, format_item


def format_competitors() -> str:
    data = collect_competitor_news()

    lines = [
        "🚗 Новости конкурентов",
        "━━━━━━━━━━━━━━━━━━",
        ""
    ]

    for company, items in data.items():
        lines.append(f"🚗 {company}")
        lines.append("")

        if not items:
            lines.append("Новостей не найдено.")
            lines.append("")
            continue

        for i, item in enumerate(items, 1):
            lines.append(format_item(item, i))

        lines.append("")

    return "\n".join(lines)
