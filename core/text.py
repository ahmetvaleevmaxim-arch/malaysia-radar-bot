import html
import re
import requests


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = html.unescape(text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def short_text(text: str, limit: int = 120) -> str:
    text = clean_text(text)

    if len(text) <= limit:
        return text

    return text[:limit].rsplit(" ", 1)[0] + "..."


def translate_to_ru(text: str) -> str:
    if not text:
        return ""

    try:
        response = requests.get(
            "https://translate.googleapis.com/translate_a/single",
            params={
                "client": "gtx",
                "sl": "auto",
                "tl": "ru",
                "dt": "t",
                "q": text,
            },
            timeout=10,
        )
        data = response.json()
        return "".join(part[0] for part in data[0] if part[0]).strip()
    except Exception:
        return text


def ru_title(text: str, limit: int = 100) -> str:
    return short_text(translate_to_ru(text), limit=limit)


def click(url: str) -> str:
    if not url:
        return ""

    return f'<a href="{url}">КЛИК</a>'
