import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, TELEGRAM_CHAT_ID, REPORT_HOUR, REPORT_MINUTE
from database import init_database

from modules.weather import format_weather
from modules.currency import format_currency
from modules.news import format_news
from modules.calendar_events import format_calendar
from modules.report import build_daily_report

from scheduler import (
    collect_all_job,
    collect_news_job,
    collect_weather_job,
    collect_currency_job,
    collect_competitors_job,
    collect_maxim_job,
)


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
        await message.answer(part, disable_web_page_preview=True)


async def send_long_to_chat(bot: Bot, chat_id: str, text: str):
    for part in split_message(text):
        await bot.send_message(
            chat_id,
            part,
            disable_web_page_preview=True
        )


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🇲🇾 Malaysia Radar Bot запущен.\n\n"
        f"Ваш chat_id: {message.chat.id}\n\n"
        "Команды:\n"
        "/weather — погода\n"
        "/currency — курсы валют\n"
        "/news — новости\n"
        "/calendar — календарь праздников и событий\n"
        "/report — полный отчет\n"
        "/collect — вручную собрать данные\n"
        "/help — помощь"
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "🇲🇾 Malaysia Radar\n\n"
        "Бот собирает информацию по Малайзии и вашим городам:\n"
        "Miri, Bintulu, Labuan, Sibu, Seremban.\n\n"
        "Команды:\n"
        "/weather — текущая погода и прогноз на 3 часа\n"
        "/currency — курсы валют\n"
        "/news — новости страны, городов, конкурентов и Maxim\n"
        "/calendar — праздники и события\n"
        "/report — полный ежедневный отчет\n"
        "/collect — вручную обновить данные"
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
    await send_long(message, format_calendar())


@dp.message(Command("report"))
async def report(message: Message):
    await message.answer("📊 Собираю полный отчет...")
    await send_long(message, build_daily_report())


@dp.message(Command("collect"))
async def collect(message: Message):
    await message.answer("🔄 Начинаю ручной сбор данных...")

    try:
        important_mentions = collect_all_job()

        text = "✅ Сбор данных завершен."

        if important_mentions:
            text += "\n\n🚨 Найдены важные упоминания Maxim:\n\n"

            for item in important_mentions:
                text += (
                    f"• {item.get('title', '')}\n"
                    f"Город: {item.get('city', 'Malaysia')}\n"
                    f"Категория: {item.get('category', 'упоминание')}\n"
                    f"Важность: {item.get('priority', 0)}/5\n"
                    f"Ссылка: {item.get('url', '')}\n\n"
                )

        await send_long(message, text)

    except Exception as e:
        await message.answer(f"❌ Ошибка при сборе данных:\n{e}")


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is empty. Add it to .env file.")

    init_database()

    bot = Bot(BOT_TOKEN)

    scheduler = AsyncIOScheduler(timezone="Asia/Kuala_Lumpur")

    async def daily_report_job():
        if TELEGRAM_CHAT_ID:
            report_text = build_daily_report()
            await send_long_to_chat(bot, TELEGRAM_CHAT_ID, report_text)

    async def collect_all_scheduler_job():
        important_mentions = collect_all_job()

        if TELEGRAM_CHAT_ID and important_mentions:
            text = "🚨 Важные упоминания Maxim\n\n"

            for item in important_mentions:
                text += (
                    f"• {item.get('title', '')}\n"
                    f"Город: {item.get('city', 'Malaysia')}\n"
                    f"Категория: {item.get('category', 'упоминание')}\n"
                    f"Важность: {item.get('priority', 0)}/5\n"
                    f"Ссылка: {item.get('url', '')}\n\n"
                )

            await send_long_to_chat(bot, TELEGRAM_CHAT_ID, text)

    scheduler.add_job(collect_news_job, "interval", minutes=30)
    scheduler.add_job(collect_weather_job, "interval", minutes=30)
    scheduler.add_job(collect_currency_job, "interval", hours=12)
    scheduler.add_job(collect_competitors_job, "interval", hours=1)
    scheduler.add_job(collect_all_scheduler_job, "interval", minutes=30)
    scheduler.add_job(collect_maxim_job, "interval", minutes=15)

    if TELEGRAM_CHAT_ID:
        scheduler.add_job(
            daily_report_job,
            "cron",
            hour=REPORT_HOUR,
            minute=REPORT_MINUTE
        )

    scheduler.start()

    print("Malaysia Radar Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
