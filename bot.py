import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, TELEGRAM_CHAT_ID, REPORT_HOUR, REPORT_MINUTE
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
        await message.answer(part, disable_web_page_preview=True)


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🇲🇾 Malaysia Radar Bot запущен.\n\n"
        f"Ваш chat_id: {message.chat.id}\n\n"
        "Команды:\n"
        "/weather — погода\n"
        "/currency — курсы валют\n"
        "/news — новости\n"
        "/calendar — календарь\n"
        "/report — полный отчет\n"
        "/help — помощь"
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Команды Malaysia Radar:\n\n"
        "/weather — погода по Miri, Bintulu, Labuan, Sibu, Seremban\n"
        "/currency — MYR/USD/RUB/EUR/SGD\n"
        "/news — новости по стране и городам\n"
        "/calendar — праздники и события на 14 дней\n"
        "/report — общий отчет"
    )


@dp.message(Command("weather"))
async def weather(message: Message):
    await message.answer("Собираю погоду...")
    await send_long(message, format_weather())


@dp.message(Command("currency"))
async def currency(message: Message):
    await message.answer("Собираю курсы валют...")
    await send_long(message, format_currency())


@dp.message(Command("news"))
async def news(message: Message):
    await message.answer("Собираю новости...")
    await send_long(message, format_news())


@dp.message(Command("calendar"))
async def calendar(message: Message):
    await send_long(message, format_calendar())


@dp.message(Command("report"))
async def report(message: Message):
    await message.answer("Собираю полный отчет...")
    await send_long(message, build_daily_report())


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is empty. Add it to .env file.")

    bot = Bot(BOT_TOKEN)

    scheduler = AsyncIOScheduler(timezone="Asia/Kuala_Lumpur")

    async def daily_report_job():
        if TELEGRAM_CHAT_ID:
            report_text = build_daily_report()
            for part in split_message(report_text):
                await bot.send_message(TELEGRAM_CHAT_ID, part, disable_web_page_preview=True)

    if TELEGRAM_CHAT_ID:
        scheduler.add_job(daily_report_job, "cron", hour=REPORT_HOUR, minute=REPORT_MINUTE)
        scheduler.start()

    print("Malaysia Radar Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
