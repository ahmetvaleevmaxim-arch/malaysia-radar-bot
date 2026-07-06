#!/bin/bash

echo "======================================="
echo "🇲🇾 Malaysia Radar"
echo "======================================="

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено."
    exit 1
fi

source venv/bin/activate

echo "📦 Проверка зависимостей..."
pip install -r requirements.txt

echo "🗄 Инициализация базы..."
python3 database.py

echo "🚀 Запуск бота..."
python3 bot.py
