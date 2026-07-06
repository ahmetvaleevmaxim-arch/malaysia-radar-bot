from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎯 Action Center"),
                KeyboardButton(text="🌅 Morning Brief"),
            ],
            [
                KeyboardButton(text="📰 Новости"),
                KeyboardButton(text="📍 Города"),
            ],
            [
                KeyboardButton(text="🚗 Конкуренты"),
                KeyboardButton(text="🚨 Maxim"),
            ],
            [
                KeyboardButton(text="🌦 Погода"),
                KeyboardButton(text="💰 Валюты"),
            ],
            [
                KeyboardButton(text="ℹ️ Помощь"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите раздел",
    )
