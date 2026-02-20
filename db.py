# db.py
import psycopg2
import pandas as pd
from contextlib import contextmanager
from config import DB_CONFIG


# -----------------------------
# Connection manager
# -----------------------------
@contextmanager
def get_conn():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()


# -----------------------------
# Fetch data as Pandas DataFrame (for dashboard)
# -----------------------------
def fetch_df(query, params=None):
    with get_conn() as conn:
        return pd.read_sql(query, conn, params=params)


# -----------------------------
# Fetch raw rows (for pipelines)
# -----------------------------
def fetch_all(query, params=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()


# -----------------------------
# Execute INSERT / UPDATE / DELETE
# -----------------------------
def execute(query, params=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            conn.commit()