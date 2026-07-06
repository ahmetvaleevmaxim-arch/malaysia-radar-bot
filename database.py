import sqlite3
from pathlib import Path

from config import DATABASE_NAME

# ==========================================
# Создаем папку data
# ==========================================

Path("data").mkdir(exist_ok=True)


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    # ==========================================
    # Новости
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        city TEXT,

        title TEXT,

        summary TEXT,

        source TEXT,

        url TEXT UNIQUE,

        published TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ==========================================
    # Погода
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        city TEXT,

        temperature REAL,

        weather TEXT,

        humidity INTEGER,

        wind REAL,

        rain REAL,

        forecast_1h TEXT,

        forecast_2h TEXT,

        forecast_3h TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ==========================================
    # Валюты
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS currency (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usd REAL,

        eur REAL,

        rub REAL,

        cny REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ==========================================
    # Конкуренты
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS competitors (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company TEXT,

        title TEXT,

        summary TEXT,

        url TEXT UNIQUE,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ==========================================
    # Maxim Monitor
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS maxim_monitor (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        platform TEXT,

        city TEXT,

        category TEXT,

        author TEXT,

        text TEXT,

        url TEXT UNIQUE,

        priority INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ==========================================
    # Праздники
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS holidays (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        city TEXT,

        title TEXT,

        holiday_date TEXT,

        description TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ==========================================
    # Мероприятия
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        city TEXT,

        title TEXT,

        event_date TEXT,

        place TEXT,

        url TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ==========================================
    # История отчетов
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        report_date TEXT,

        report_text TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print("✅ База данных успешно создана.")
