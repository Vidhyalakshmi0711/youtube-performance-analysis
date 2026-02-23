# db.py
import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Connection Pool (IMPORTANT)
neon_pool = psycopg2.pool.SimpleConnectionPool(
    1, 5,   # min 1, max 5 connections
    os.getenv("NEON_DB_URL")
)

def get_conn():
    return neon_pool.getconn()

def release_conn(conn):
    neon_pool.putconn(conn)

def fetch_df(query):
    conn = get_conn()
    df = pd.read_sql(query, conn)
    release_conn(conn)
    return df