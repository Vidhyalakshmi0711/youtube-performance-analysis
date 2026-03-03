# config.py
import os
import psycopg2
from urllib.parse import urlparse

# -------------------------------
# PARSE NEON DATABASE URL
# -------------------------------
NEON_DB_URL = os.getenv("NEON_DB_URL_WRITE")

if not NEON_DB_URL:
    raise ValueError("NEON_DB_URL is missing. Add it to your .env or GitHub secrets.")

url = urlparse(NEON_DB_URL)

DB_HOST = url.hostname
DB_NAME = url.path.lstrip("/")
DB_USER = url.username
DB_PASSWORD = url.password
DB_PORT = url.port or 5432  # Neon defaults to 5432

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT,
    sslmode="require"
)

# -------------------------------
# YOUTUBE API KEY
# -------------------------------
API_KEY = os.getenv("YOUTUBE_API_KEY")

