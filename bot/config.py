import os
from pathlib import Path
from dotenv import load_dotenv

# Loyiha ildizidagi .env ni o'qish
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/api/v1").rstrip("/")
BOT_API_SECRET = os.getenv("BOT_API_SECRET", "dev-bot-api-secret-key")
