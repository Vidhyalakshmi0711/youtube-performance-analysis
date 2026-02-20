# streamlit_app.py
import streamlit as st
import pandas as pd
from db import fetch_df
from config import API_KEY  # YouTube API key from Neon/Streamlit secrets

st.set_page_config(page_title="YouTube Performance Analysis", layout="wide")
st.title("YouTube Performance Analysis Dashboard")

# ----------------------------
# Fetch Channels
# ----------------------------
channels_data = fetch_df("SELECT * FROM channels")
if channels_data:
    channels_df = pd.DataFrame(channels_data, columns=["channel_id", "channel_name"])
else:
    channels_df = pd.DataFrame(columns=["channel_id", "channel_name"])

st.subheader("Channels")
st.dataframe(channels_df)

# ----------------------------
# Fetch Video Master
# ----------------------------
video_master_data = fetch_df("SELECT * FROM video_master")
if video_master_data:
    video_master_df = pd.DataFrame(
        video_master_data,
        columns=["published_at", "video_id", "title", "channel_id", "channel_name"]
    )
    # Drop columns we don't need for display
    video_master_clean = video_master_df.drop(columns=["channel_id", "channel_name"], errors="ignore")
else:
    video_master_clean = pd.DataFrame(columns=["published_at", "video_id", "title"])

st.subheader("Video Master")
st.dataframe(video_master_clean)

# ----------------------------
# Fetch Video Daily Stats
# ----------------------------
video_stats_data = fetch_df("SELECT * FROM video_daily_stats")
if video_stats_data:
    video_stats_df = pd.DataFrame(
        video_stats_data,
        columns=["likes", "views", "date", "comments", "video_id", "channel_name", "channel_id"]
    )
else:
    video_stats_df = pd.DataFrame(columns=["likes", "views", "date", "comments", "video_id", "channel_name", "channel_id"])

st.subheader("Video Daily Stats")
st.dataframe(video_stats_df)

# ----------------------------
# Example Analysis: Top 5 Videos by Total Views
# ----------------------------
if not video_stats_df.empty:
    top_videos = (
        video_stats_df.groupby("video_id")["views"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    st.subheader("Top 5 Videos by Total Views")
    st.dataframe(top_videos)

# ----------------------------
# YouTube API Key (hidden)
# ----------------------------
st.subheader("YouTube API Key Loaded")
st.write("API Key loaded successfully. (Hidden for security)")