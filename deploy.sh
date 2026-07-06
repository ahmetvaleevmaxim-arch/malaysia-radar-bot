#!/bin/bash

echo "======================================="
echo "🚀 Deploy Malaysia Radar"
echo "======================================="

cd "$(dirname "$0")"

echo "📥 Получение обновлений..."
git pull

echo "📦 Обновление зависимостей..."
source venv/bin/activate
pip install -r requirements.txt

echo "🗄 Обновление базы..."
python3 database.py

echo "✅ Deploy завершен."
echo ""
echo "Для запуска выполните:"
echo "./run.sh"
