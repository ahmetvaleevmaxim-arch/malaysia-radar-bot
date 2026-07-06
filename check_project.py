print("Проверка Malaysia Radar...")

print("1. Проверяю config.py")
import config

print("2. Проверяю database.py")
import database

print("3. Проверяю services")
from services.news_service import collect_country_news, collect_all_city_news
from services.weather_service import get_all_weather
from services.currency_service import get_currency_rates
from services.competitor_service import get_all_competitors
from services.maxim_service import get_maxim_mentions
from services.holiday_service import get_calendar
from services.report_service import build_report
from services.database_service import save_news

print("4. Проверяю modules")
from modules.news import format_news
from modules.weather import format_weather
from modules.currency import format_currency
from modules.calendar_events import format_calendar
from modules.report import build_daily_report

print("5. Проверяю bot.py")
import bot

print("✅ Проверка завершена. Импорты работают.")
