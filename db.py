# db.py
import streamlit as st
import psycopg2
from psycopg2 import sql
from config import conn

# Utility function to execute SELECT queries
def fetch_df(query, params=None):
    """
    Execute a SELECT query and return all results.
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            result = cur.fetchall()
        return result
    except psycopg2.Error as e:
        st.error(f"Database error (fetch_df): {e}")
        conn.rollback()  # Reset failed transaction
        return []

# Utility function to execute INSERT/UPDATE/DELETE queries
def execute_query(query, params=None):
    """
    Execute an INSERT/UPDATE/DELETE query safely.
    Returns True if successful, False otherwise.
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
        return True
    except psycopg2.Error as e:
        st.error(f"Database error (execute_query): {e}")
        conn.rollback()  # Reset failed transaction
        return False

# Example usage functions
def insert_youtube_channel(channel_id, channel_name, subscribers):
    """
    Inserts a YouTube channel into the DB.
    """
    query = """
    INSERT INTO youtube_channels (channel_id, channel_name, subscribers)
    VALUES (%s, %s, %s)
    """
    return execute_query(query, (channel_id, channel_name, subscribers))

def get_all_channels():
    """
    Fetch all YouTube channels from the DB.
    """
    query = "SELECT * FROM youtube_channels ORDER BY subscribers DESC"
    return fetch_df(query)

