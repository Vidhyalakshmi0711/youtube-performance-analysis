# db.py
import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import pandas as pd


load_dotenv()

# -----------------------------------------
# Use correct Neon DB URL (NOT admin URL)
# -----------------------------------------
DATABASE_URL = os.getenv("NEON_DB_URL")

# -----------------------------------------
# Larger Pool for Streamlit
# -----------------------------------------
neon_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,   # increased from 5
    dsn=DATABASE_URL
)

# -----------------------------------------
# Get / Release Connection
# -----------------------------------------
def get_conn():
    return neon_pool.getconn()

def release_conn(conn):
    neon_pool.putconn(conn)

# -----------------------------------------
# FETCH ALL
# -----------------------------------------
def fetch_all(query, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    finally:
        release_conn(conn)

# -----------------------------------------
# EXECUTE (INSERT / UPDATE)
# -----------------------------------------
def execute_query(query, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
    finally:
        release_conn(conn)

# -----------------------------------------
# FETCH DATAFRAME (Streamlit safe)
# -----------------------------------------
def fetch_df(query, params=None):
    conn = get_conn()
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    finally:
        release_conn(conn)


