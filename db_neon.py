import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_neon_conn():
    return psycopg2.connect(os.getenv("NEON_DB_URL"))

def get_admin_conn():
    return psycopg2.connect(os.getenv("NEON_ADMIN_URL"))