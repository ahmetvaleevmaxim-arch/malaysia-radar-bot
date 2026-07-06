import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import BOT_TOKEN, TELEGRAM_CHAT_ID, REPORT_HOUR, REPORT_MINUTE, REPORT_TIMEZONE
from database import init_database

from ui.keyboards import main_keyboard
from reports.collector import collect_all_events
from reports.morning_brief import (
    build_morning_brief,
    build_action_center,
    build_country_news,
    build_city_news,
    build_competitors,
    build_maxim,
    build_weather,
    build_currency,
)


logging.basicConfig(level=logging.INFO)

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
            disable_web_page_preview=True,
            reply_markup=main_keyboard(),
            parse_mode="HTML",
        )


def collect_events_safe():
    try:
        return collect_all_events()
    except Exception as e:
        logging.exception("Ошибка сбора данных")
        return []


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🇲🇾 Malaysia Radar 2.0\n\n"
        "Операционная сводка для развития Малайзии.\n\n"
        "Используйте кнопки ниже.\n\n"
        f"Ваш chat_id: {message.chat.id}",
        reply_markup=main_keyboard(),
    )


@dp.message(Command("help"))
@dp.message(F.text == "ℹ️ Помощь")
async def help_command(message: Message):
    await message.answer(
        "🇲🇾 Malaysia Radar 2.0\n\n"
        "Разделы:\n"
        "🎯 Action Center — что требует внимания\n"
        "🌅 Morning Brief — полная утренняя сводка\n"
        "📰 Новости — новости Малайзии за сегодня\n"
        "📍 Города — новости по Miri, Bintulu, Labuan, Sibu, Seremban\n"
        "🚗 Конкуренты — Grab, inDrive, Bolt, AirAsia Ride, MyRide\n"
        "🚨 Maxim — упоминания Maxim e-hailing Malaysia\n"
        "🌦 Погода — текущая ситуация и прогноз\n"
        "💰 Валюты — основные курсы",
        reply_markup=main_keyboard(),
    )


@dp.message(Command("report"))
@dp.message(F.text == "🌅 Morning Brief")
async def morning_brief(message: Message):
    await message.answer("🌅 Собираю Morning Brief...", reply_markup=main_keyboard())
    events = collect_events_safe()
    await send_long(message, build_morning_brief(events))


@dp.message(F.text == "🎯 Action Center")
async def action_center(message: Message):
    await message.answer("🎯 Проверяю важные события...", reply_markup=main_keyboard())
    events = collect_events_safe()
    await send_long(message, "\n".join(build_action_center(events)))


@dp.message(Command("news"))
@dp.message(F.text == "📰 Новости")
async def country_news(message: Message):
    await message.answer("📰 Собираю новости Малайзии за сегодня...", reply_markup=main_keyboard())
    events = collect_events_safe()
    await send_long(message, "\n".join(build_country_news(events)))


@dp.message(F.text == "📍 Города")
async def city_news(message: Message):
    await message.answer("📍 Собираю новости городов за сегодня...", reply_markup=main_keyboard())
    events = collect_events_safe()
    await send_long(message, "\n".join(build_city_news(events)))


@dp.message(F.text == "🚗 Конкуренты")
async def competitors(message: Message):
    await message.answer("🚗 Проверяю конкурентов за сегодня...", reply_markup=main_keyboard())
    events = collect_events_safe()
    await send_long(message, "\n".join(build_competitors(events)))


@dp.message(F.text == "🚨 Maxim")
async def maxim(message: Message):
    await message.answer("🚨 Проверяю Maxim e-hailing Malaysia...", reply_markup=main_keyboard())
    events = collect_events_safe()
    await send_long(message, "\n".join(build_maxim(events)))


@dp.message(Command("weather"))
@dp.message(F.text == "🌦 Погода")
async def weather(message: Message):
    await message.answer("🌦 Собираю погоду...", reply_markup=main_keyboard())
    events = collect_events_safe()
    await send_long(message, "\n".join(build_weather(events)))


@dp.message(Command("currency"))
@dp.message(F.text == "💰 Валюты")
async def currency(message: Message):
    await message.answer("💰 Собираю валюты...", reply_markup=main_keyboard())
    events = collect_events_safe()
    await send_long(message, "\n".join(build_currency(events)))


@dp.message()
async def unknown(message: Message):
    await message.answer(
        "Выберите нужный раздел кнопками ниже.",
        reply_markup=main_keyboard(),
    )


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is empty. Add it to .env file.")

    init_database()

    bot = Bot(BOT_TOKEN)

        scheduler = AsyncIOScheduler(timezone=REPORT_TIMEZONE)

    async def morning_report_job():
        if not TELEGRAM_CHAT_ID:
            logging.warning("TELEGRAM_CHAT_ID is empty. Morning report skipped.")
            return

        events = collect_events_safe()
        report_text = build_morning_brief(events)

        for part in split_message(report_text):
            await bot.send_message(
                TELEGRAM_CHAT_ID,
                part,
                disable_web_page_preview=True,
                parse_mode="HTML",
            )

    scheduler.add_job(
        morning_report_job,
        "cron",
        hour=REPORT_HOUR,
        minute=REPORT_MINUTE,
    )

    scheduler.start()

    logging.info(
        f"Morning report scheduled at {REPORT_HOUR:02d}:{REPORT_MINUTE:02d} {REPORT_TIMEZONE}"
    )

    logging.info("Malaysia Radar 2.0 started")
    logging.info("Polling started")

    await dp.start_polling(
        bot,
        handle_signals=False,
    )


if __name__ == "__main__":
    asyncio.run(main())
