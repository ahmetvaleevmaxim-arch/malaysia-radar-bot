import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

REPORT_HOUR = int(os.getenv("REPORT_HOUR", "8"))
REPORT_MINUTE = int(os.getenv("REPORT_MINUTE", "0"))

CITIES = {
    "Miri": {"lat": 4.3995, "lon": 113.9914, "keywords": ["Miri"]},
    "Bintulu": {"lat": 3.1703, "lon": 113.0419, "keywords": ["Bintulu"]},
    "Labuan": {"lat": 5.2831, "lon": 115.2308, "keywords": ["Labuan"]},
    "Sibu": {"lat": 2.2873, "lon": 111.8305, "keywords": ["Sibu"]},
    "Seremban": {"lat": 2.7297, "lon": 101.9381, "keywords": ["Seremban", "Negeri Sembilan"]},
}

NEWS_SOURCES = {
    "Malaysia": [
        "https://www.thestar.com.my/rss/news/nation",
        "https://www.malaymail.com/feed/rss/malaysia",
        "https://www.nst.com.my/rss/news",
        "https://www.freemalaysiatoday.com/category/nation/feed/",
    ],
    "Borneo": [
        "https://www.theborneopost.com/feed/",
    ],
}
