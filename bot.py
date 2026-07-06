import asyncio
from typing import Callable

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, TELEGRAM_CHAT_ID, REPORT_HOUR, REPORT_MINUTE
from modules.weather import format_weather
from modules.currency import format_currency
from modules.news import format_news
from modules.calendar_events import format_calendar
from modules.report import build_daily_report


dp = Dispatcher()


def split_message(text: str, max_len: int = 3900) -> list[str]:
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


async def send_long_message(message: Message, text: str):
    for part in split_message(text):
        await message.answer(part, disable_web_page_preview=True)


async def send_long_callback(callback: CallbackQuery, text: str):
    if callback.message:
        for part in split_message(text):
            await callback.message.answer(part, disable_web_page_preview=True)


def main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.button(text="📰 Новости", callback_data="menu_news")
    kb.button(text="🌦 Погода", callback_data="menu_weather")

    kb.button(text="💰 Валюты", callback_data="menu_currency")
    kb.button(text="📅 Праздники и события", callback_data="menu_calendar")

    kb.button(text="📊 Полный отчет", callback_data="menu_report")
    kb.button(text="ℹ️ Помощь", callback_data="menu_help")

    kb.adjust(2)
    return kb.as_markup()


def back_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад в меню", callback_data="menu_main")
    return kb.as_markup()


def start_text(message: Message | None = None) -> str:
    chat_id_line = ""
    if message:
        chat_id_line = f"\n\nВаш chat_id: `{message.chat.id}`"

    return (
        "🇲🇾 **Malaysia Radar**\n\n"
        "Бот для ежедневного мониторинга Малайзии и ваших 5 городов:\n"
        "Miri, Bintulu, Labuan, Sibu, Seremban.\n\n"
        "Выберите раздел кнопками ниже."
        f"{chat_id_line}"
    )


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        start_text(message),
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "ℹ️ **Помощь**\n\n"
        "Доступные команды:\n\n"
        "/start — открыть главное меню\n"
        "/weather — погода по городам\n"
        "/currency — курсы валют\n"
        "/news — новости\n"
        "/calendar — праздники и события\n"
        "/report — полный отчет\n\n"
        "Основной режим работы — через кнопки.",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )


@dp.message(Command("weather"))
async def weather(message: Message):
    await message.answer("🌦 Собираю погоду...")
    await send_long_message(message, format_weather())


@dp.message(Command("currency"))
async def currency(message: Message):
    await message.answer("💰 Собираю курсы валют...")
    await send_long_message(message, format_currency())


@dp.message(Command("news"))
async def news(message: Message):
    await message.answer("📰 Собираю новости...")
    await send_long_message(message, format_news())


@dp.message(Command("calendar"))
async def calendar(message: Message):
    await send_long_message(message, format_calendar())


@dp.message(Command("report"))
async def report(message: Message):
    await message.answer("📊 Собираю полный отчет...")
    await send_long_message(message, build_daily_report())


@dp.callback_query(F.data == "menu_main")
async def callback_main(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🇲🇾 **Malaysia Radar**\n\nВыберите нужный раздел.",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )


@dp.callback_query(F.data == "menu_help")
async def callback_help(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "ℹ️ **Помощь**\n\n"
        "Бот собирает информацию по Малайзии и вашим городам.\n\n"
        "Разделы:\n"
        "📰 Новости — страна и города\n"
        "🌦 Погода — текущая и прогноз\n"
        "💰 Валюты — основные курсы\n"
        "📅 Праздники и события — ближайшие даты\n"
        "📊 Полный отчет — вся сводка сразу\n\n"
        "Все данные выводятся на русском.",
        reply_markup=back_menu(),
        parse_mode="Markdown"
    )


async def handle_section(
    callback: CallbackQuery,
    loading_text: str,
    formatter: Callable[[], str],
):
    await callback.answer()
    if callback.message:
        await callback.message.edit_text(loading_text)
        result = formatter()
        await callback.message.answer(
            result,
            reply_markup=back_menu(),
            disable_web_page_preview=True
        )


@dp.callback_query(F.data == "menu_news")
async def callback_news(callback: CallbackQuery):
    await handle_section(callback, "📰 Собираю новости...", format_news)


@dp.callback_query(F.data == "menu_weather")
async def callback_weather(callback: CallbackQuery):
    await handle_section(callback, "🌦 Собираю погоду...", format_weather)


@dp.callback_query(F.data == "menu_currency")
async def callback_currency(callback: CallbackQuery):
    await handle_section(callback, "💰 Собираю курсы валют...", format_currency)


@dp.callback_query(F.data == "menu_calendar")
async def callback_calendar(callback: CallbackQuery):
    await handle_section(callback, "📅 Собираю праздники и события...", format_calendar)


@dp.callback_query(F.data == "menu_report")
async def callback_report(callback: CallbackQuery):
    await handle_section(callback, "📊 Собираю полный отчет...", build_daily_report)


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is empty. Add it to .env file.")

    bot = Bot(BOT_TOKEN)
    scheduler = AsyncIOScheduler(timezone="Asia/Kuala_Lumpur")

    async def daily_report_job():
        if TELEGRAM_CHAT_ID:
            report_text = build_daily_report()
            for part in split_message(report_text):
                await bot.send_message(
                    TELEGRAM_CHAT_ID,
                    part,
                    disable_web_page_preview=True
                )

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
