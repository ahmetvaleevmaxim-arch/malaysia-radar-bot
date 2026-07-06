import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# Telegram
# ==========================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

# ==========================================
# Daily Report
# ==========================================

REPORT_HOUR = int(os.getenv("REPORT_HOUR", "8"))
REPORT_MINUTE = int(os.getenv("REPORT_MINUTE", "0"))

# ==========================================
# Malaysia Cities
# ==========================================

CITIES = {
    "Miri": {
        "lat": 4.3995,
        "lon": 113.9914,
        "state": "Sarawak",
        "keywords": [
            "Miri"
        ]
    },

    "Bintulu": {
        "lat": 3.1703,
        "lon": 113.0419,
        "state": "Sarawak",
        "keywords": [
            "Bintulu"
        ]
    },

    "Labuan": {
        "lat": 5.2831,
        "lon": 115.2308,
        "state": "Labuan",
        "keywords": [
            "Labuan"
        ]
    },

    "Sibu": {
        "lat": 2.2873,
        "lon": 111.8305,
        "state": "Sarawak",
        "keywords": [
            "Sibu"
        ]
    },

    "Seremban": {
        "lat": 2.7297,
        "lon": 101.9381,
        "state": "Negeri Sembilan",
        "keywords": [
            "Seremban",
            "Negeri Sembilan"
        ]
    }
}

# ==========================================
# News Sources
# ==========================================

NEWS_SOURCES = {
    "Malaysia": [
        "https://www.thestar.com.my/rss/news/nation",
        "https://www.malaymail.com/feed/rss/malaysia",
        "https://www.nst.com.my/rss/news",
        "https://www.freemalaysiatoday.com/category/nation/feed/",
        "https://www.bernama.com/en/rss.php",
        "https://www.malaysiakini.com/rss/en/news",
        "https://www.malaysianow.com/feed",
        "https://www.theedgemalaysia.com/rss",
        "https://www.sinarharian.com.my/rssFeed/10",
        "https://www.hmetro.com.my/utama.xml",
    ],

    "Borneo": [
        "https://www.theborneopost.com/feed/",
        "https://www.newsarawaktribune.com.my/feed/",
        "https://www.utusanborneo.com.my/rss.xml",
    ]
}

# ==========================================
# Competitors
# ==========================================

COMPETITORS = {
    "Grab": [
        "Grab Malaysia",
        "Grab Driver Malaysia",
        "Grab promo"
    ],

    "inDrive": [
        "inDrive Malaysia",
        "inDrive Driver Malaysia"
    ],

    "Bolt": [
        "Bolt Malaysia"
    ],

    "AirAsia Ride": [
        "AirAsia Ride"
    ],

    "MyRide": [
        "MyRide Malaysia"
    ]
}

# ==========================================
# Maxim Monitor
# ==========================================

MAXIM_KEYWORDS = [

    "Maxim",

    "Maxim Malaysia",

    "Maxim Miri",

    "Maxim Bintulu",

    "Maxim Labuan",

    "Maxim Sibu",

    "Maxim Seremban",

    "Maxim e-hailing",

    "Maxim driver",

    "Maxim teksi"

]

# ==========================================
# Social Networks
# ==========================================

SOCIAL_NETWORKS = [
    "Facebook",
    "Threads",
    "Instagram",
    "TikTok",
    "Reddit",
    "X",
    "YouTube",
    "Google News"
]

# ==========================================
# Scheduler
# ==========================================

CHECK_NEWS_EVERY = 30
CHECK_WEATHER_EVERY = 30
CHECK_COMPETITORS_EVERY = 60
CHECK_SOCIAL_EVERY = 15

# ==========================================
# Database
# ==========================================

DATABASE_NAME = "data/malaysia_radar.db"

# ==========================================
# Logs
# ==========================================

LOG_FILE = "logs/radar.log"
