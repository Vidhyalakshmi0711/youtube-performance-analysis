# db.py
from config import conn

def get_data(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
