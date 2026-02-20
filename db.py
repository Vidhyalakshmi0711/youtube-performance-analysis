# db.py
from config import conn

def fetch_df(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

