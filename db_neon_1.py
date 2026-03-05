#db.py
import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# -----------------------------------------
# USE ROLE-BASED DB CONNECTIONS
# -----------------------------------------
DB_WRITE = os.getenv("NEON_DB_URL_WRITE")   # neondb_owner
DB_READ  = os.getenv("NEON_DB_URL_READ")    # yt_dashboard_ro

# -----------------------------------------
# CONNECTION POOLS
# -----------------------------------------
pool_write = psycopg2.pool.SimpleConnectionPool(
    minconn=1, maxconn=5, dsn=DB_WRITE
)

pool_read = psycopg2.pool.SimpleConnectionPool(
    minconn=1, maxconn=10, dsn=DB_READ
)

def get_conn_write():
    return pool_write.getconn()

def release_conn_write(conn):
    pool_write.putconn(conn)

def get_conn_read():
    return pool_read.getconn()

def release_conn_read(conn):
    pool_read.putconn(conn)

# -----------------------------------------
# WRITE / UPSERT
# -----------------------------------------
def execute_query(query, params=None):
    conn = get_conn_write()
    cur = conn.cursor()

    cur.execute("SELECT current_user;")
    print("🔎 Connected as:", cur.fetchone()[0])

    try:
        cur.execute(query, params)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        release_conn_write(conn)

# -----------------------------------------
# READ FOR DASHBOARD
# -----------------------------------------
def fetch_all(query, params=None):
    conn = get_conn_read()
    cur = conn.cursor()
    try:
        cur.execute(query, params)
        return cur.fetchall()  # <-- list of tuples
    finally:
        columns = [desc[0] for desc in cur.description]   #<------changed here
        cur.close()
        release_conn_read(conn)

