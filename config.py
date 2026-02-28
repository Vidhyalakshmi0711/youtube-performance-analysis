# config.py
import os
import psycopg2
import streamlit as st


# ---------------------------------------------------
# ENVIRONMENT DETECTION
# ---------------------------------------------------
try:
    import streamlit as st
    STREAMLIT_MODE = True
except ModuleNotFoundError:
    STREAMLIT_MODE = False


# ---------------------------------------------------
# LOAD VARIABLES
# ---------------------------------------------------
if STREAMLIT_MODE:
    DB_HOST = st.secrets["DB_HOST"]
    DB_NAME = st.secrets["DB_NAME"]
    DB_USER = st.secrets["DB_USER"]
    DB_PASSWORD = st.secrets["DB_PASSWORD"]
    DB_PORT = st.secrets["DB_PORT"]
    API_KEY = st.secrets["YOUTUBE_API_KEY"]
else:
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT")
    API_KEY = os.getenv("YOUTUBE_API_KEY")


# ---------------------------------------------------
# DATABASE CONNECTION FUNCTION
# ---------------------------------------------------
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        sslmode="require"
    )


