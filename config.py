import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
DATABASE_PATH = os.getenv("DATABASE_PATH", "sega_foot_analyst.db")
