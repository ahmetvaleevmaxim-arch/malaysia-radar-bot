import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from config import BOT_TOKEN
from database import init_database

from modules.weather import format_weather
from modules.currency import format_currency
from modules.news import (
    format_news,
    format_competitor_news,
    format_maxim_mentions,
)
from modules.calendar_events import format_calendar
from modules.report import build_daily_report


logging.basicConfig(level=logging.INFO)

dp = Dispatcher()


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📰 Новости"), KeyboardButton(text="🌦 Погода")],
            [KeyboardButton(text="💰 Валюты"), KeyboardButton(text="🚗 Конкуренты")],
            [KeyboardButton(text="🚨 Maxim"), KeyboardButton(text="📅 События")],
            [KeyboardButton(text="📊 Полный отчет"), KeyboardButton(text="ℹ️ Помощь")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите раздел"
    )


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
            parse_mode="HTML"
        )


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🇲🇾 Malaysia Radar Bot запущен.\n\n"
        "Теперь можно пользоваться кнопками ниже.\n\n"
        f"Ваш chat_id: {message.chat.id}",
        reply_markup=main_keyboard()
    )


@dp.message(Command("help"))
@dp.message(F.text == "ℹ️ Помощь")
async def help_command(message: Message):
    await message.answer(
        "🇲🇾 Malaysia Radar\n\n"
        "Бот собирает информацию по Малайзии и городам:\n"
        "Miri, Bintulu, Labuan, Sibu, Seremban.\n\n"
        "Разделы:\n"
        "📰 Новости — только за текущий день\n"
        "🌦 Погода — сейчас и прогноз на 3 часа\n"
        "💰 Валюты\n"
        "🚗 Конкуренты\n"
        "🚨 Maxim — упоминания Maxim e-hailing Malaysia\n"
        "📅 События\n"
        "📊 Полный отчет",
        reply_markup=main_keyboard()
    )


@dp.message(Command("weather"))
@dp.message(F.text == "🌦 Погода")
async def weather(message: Message):
    await message.answer("🌦 Собираю погоду...", reply_markup=main_keyboard())
    await send_long(message, format_weather())


@dp.message(Command("currency"))
@dp.message(F.text == "💰 Валюты")
async def currency(message: Message):
    await message.answer("💰 Собираю курсы валют...", reply_markup=main_keyboard())
    await send_long(message, format_currency())


@dp.message(Command("news"))
@dp.message(F.text == "📰 Новости")
async def news(message: Message):
    await message.answer("📰 Собираю новости за сегодня...", reply_markup=main_keyboard())
    await send_long(message, format_news())


@dp.message(Command("calendar"))
@dp.message(F.text == "📅 События")
async def calendar(message: Message):
    await message.answer("📅 Собираю праздники и мероприятия...", reply_markup=main_keyboard())
    await send_long(message, format_calendar())


@dp.message(Command("report"))
@dp.message(F.text == "📊 Полный отчет")
async def report(message: Message):
    await message.answer("📊 Собираю полный отчет...", reply_markup=main_keyboard())
    await send_long(message, build_daily_report())


@dp.message(F.text == "🚗 Конкуренты")
async def competitors(message: Message):
    await message.answer("🚗 Собираю новости конкурентов...", reply_markup=main_keyboard())
    await send_long(message, format_competitor_news())


@dp.message(F.text == "🚨 Maxim")
async def maxim(message: Message):
    await message.answer("🚨 Проверяю упоминания Maxim e-hailing Malaysia...", reply_markup=main_keyboard())
    await send_long(message, format_maxim_mentions())


@dp.message()
async def unknown(message: Message):
    await message.answer(
        "Выберите нужный раздел кнопками ниже.",
        reply_markup=main_keyboard()
    )


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is empty. Add it to .env file.")

    init_database()

    bot = Bot(BOT_TOKEN)

    logging.info("Malaysia Radar Bot started")
    logging.info("Polling started")

    await dp.start_polling(
        bot,
        handle_signals=False
    )


if __name__ == "__main__":
    asyncio.run(main())
