from __future__ import annotations
from dotenv import dotenv_values

import zoneinfo
from pathlib import Path

config = dotenv_values(".env")
PAYMENT_LIFETIME = 60 * 60
TIME_ZONE = zoneinfo.ZoneInfo("Europe/Moscow")

BASE_DIR = Path(__file__).parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
MEDIA_DIR = BASE_DIR / 'media'
DATABASE_DIR = BASE_DIR / "database"
LOCALES_DIR = BASE_DIR / "src/locales"
INDEXNOW_KEY = config["INDEXNOW_KEY"]
SERVICE_NAME = config["SERVICE_NAME"]

for DIR in [LOG_DIR, MEDIA_DIR, DATABASE_DIR]:
    DIR.mkdir(exist_ok=True)

HTML_MAIN_PAGE_CONT_NOT_FOUND = f'<p><img src="https://files.catbox.moe/1ea1xp.png"/></p><b>Добро пожаловать на {SERVICE_NAME}</b><br/><br/><b>НЕУСТАНОВЛЕНА БАЗОВАЯ СТРАНИЦА</b><br/><b>Установить базовую страницу через API: <a href="/api/docs">/api/docs</a></b>'