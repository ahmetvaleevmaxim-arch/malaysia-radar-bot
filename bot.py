import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import BOT_TOKEN
from database import init_database

from modules.weather import format_weather
from modules.currency import format_currency
from modules.news import format_news
from modules.calendar_events import format_calendar
from modules.report import build_daily_report


dp = Dispatcher()


def split_message(text: str, max_len: int = 3900):
    parts = []

    while len(text) > max_len:
        cut = text.rfind("\n", 0, max_len)

        if cut == -1:
            cut = max_len

        parts.append(text[:cut])
        text = text[cut:].strip()

    if text:
        parts.append(text)

    return parts


async def send_long(message: Message, text: str):
    for part in split_message(text):
        await message.answer(
            part,
            disable_web_page_preview=True
        )


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🇲🇾 Malaysia Radar Bot запущен.\n\n"
        f"Ваш chat_id: {message.chat.id}\n\n"
        "Команды:\n"
        "/weather — погода по городам\n"
        "/currency — курсы валют\n"
        "/news — новости\n"
        "/calendar — праздники и события\n"
        "/report — полный отчет\n"
        "/collect — ручная проверка системы\n"
        "/help — помощь"
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "🇲🇾 Malaysia Radar\n\n"
        "Бот собирает информацию по Малайзии и городам:\n"
        "Miri, Bintulu, Labuan, Sibu, Seremban.\n\n"
        "Разделы:\n"
        "📰 Новости страны и городов\n"
        "🌦 Погода: текущая и прогноз на 3 часа\n"
        "💰 Валюты\n"
        "🚗 Конкуренты\n"
        "🚨 Упоминания Maxim\n"
        "📅 Праздники и мероприятия\n\n"
        "Основные команды:\n"
        "/weather\n"
        "/currency\n"
        "/news\n"
        "/calendar\n"
        "/report"
    )


@dp.message(Command("weather"))
async def weather(message: Message):
    await message.answer("🌦 Собираю погоду...")
    await send_long(message, format_weather())


@dp.message(Command("currency"))
async def currency(message: Message):
    await message.answer("💰 Собираю курсы валют...")
    await send_long(message, format_currency())


@dp.message(Command("news"))
async def news(message: Message):
    await message.answer("📰 Собираю новости...")
    await send_long(message, format_news())


@dp.message(Command("calendar"))
async def calendar(message: Message):
    await message.answer("📅 Собираю праздники и мероприятия...")
    await send_long(message, format_calendar())


@dp.message(Command("report"))
async def report(message: Message):
    await message.answer("📊 Собираю полный отчет...")
    await send_long(message, build_daily_report())


@dp.message(Command("collect"))
async def collect(message: Message):
    await message.answer(
        "✅ Бот работает.\n\n"
        "Telegram подключен.\n"
        "Команды обрабатываются.\n"
        "Следующий этап — вернуть автоматический сбор данных и уведомления."
    )


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is empty. Add it to .env file.")

    init_database()

    bot = Bot(BOT_TOKEN)

    print("Malaysia Radar Bot started")
    print("Polling started")

    await dp.start_polling(
        bot,
        handle_signals=False
    )


if __name__ == "__main__":
    asyncio.run(main())
