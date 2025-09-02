import os
from dotenv import load_dotenv

load_dotenv(".env")

API_ID = int(os.getenv("API_ID", "20124949"))
API_HASH = os.getenv("API_HASH", "ff39880b27afecc7b5063766a78591db")

BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URL = os.getenv("MONGO_URL")
NAMA_DB = os.getenv("NAMA_DB", "CashflowBot")
