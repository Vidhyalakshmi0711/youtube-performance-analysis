# config.py
import streamlit as st
import psycopg2

# Database connection
conn = psycopg2.connect(
    host=st.secrets["DB_HOST"],
    database=st.secrets["DB_NAME"],
    user=st.secrets["DB_USER"],
    password=st.secrets["DB_PASSWORD"],
    port=st.secrets["DB_PORT"],
    sslmode="require"
)

# YouTube API key
API_KEY = st.secrets["YOUTUBE_API_KEY"]
