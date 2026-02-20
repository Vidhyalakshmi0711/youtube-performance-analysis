# config.py
import os
from dotenv import load_dotenv

load_dotenv()   # load .env file

API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")   # optional

DB_CONFIG = {
    "host": "localhost",
    "database": "youtube_analytics",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "port": 5432
}
