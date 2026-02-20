import streamlit as st
import pandas as pd
import plotly.express as px
from db import fetch_df

st.set_page_config(page_title="YouTube Intelligence Dashboard", layout="wide")

# =====================
# LOAD DATA
# =====================
video_master = fetch_df("SELECT * FROM video_master")
stats = fetch_df("SELECT * FROM video_daily_stats")
channels = fetch_df("SELECT * FROM channels")

# Clean duplicates
video_master_clean = video_master.drop(columns=["channel_id", "channel_name"], errors="ignore")
df = stats.merge(video_master_clean, on="video_id", how="left")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# =====================
# SIDEBAR FILTERS
# =====================
st.sidebar.title("🎯 Filters")

channel_filter = st.sidebar.multiselect(
    "Select Channel",
    channels["channel_name"].tolist(),
    default=channels["channel_name"].tolist()
)

date_range = st.sidebar.date_input(
    "Date Range",
    [df["date"].min(), df["date"].max()]
)

# APPLY CHANNEL FILTER
df = df[df["channel_name"].isin(channel_filter)]

# APPLY DATE FILTER
start_date, end_date = date_range
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

# =====================
# HEADER STYLE
# =====================
st.markdown(
    """
    <h1 style='text-align:center; color:#FF4B4B;'>
        🔥 YouTube Intelligence Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

# =====================
# CHANNEL SELECTED BOX
# =====================
selected_channels_text = ", ".join(channel_filter)

st.markdown(
    f"""
    <div style='padding:10px; border-radius:10px; background:#E7FCEB; margin-bottom:20px;'>
        <b>📌 Channel Selected:</b> <span style='color:#008000; font-weight:700;'>{selected_channels_text}</span>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================
# KPI METRICS
# =====================
total_views = df["views"].sum()
total_likes = df["likes"].sum()
total_comments = df["comments"].sum()
total_videos = df["video_id"].nunique()

# KPI CARD STYLE
def metric_card(title, value, icon):
    st.markdown(
        f"""
        <div style="background:#1E1E1E; padding:20px; border-radius:15px; text-align:center;
                    color:white; font-size:22px; font-weight:600; box-shadow:0 4px 10px rgba(0,0,0,0.2);">
            <div style="font-size:50px;">{icon}</div>
            {title}<br>
            <span style="font-size:28px; color:#FFD700;">{value}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("Total Videos", f"{total_videos:,}", "🎬")
with col2:
    metric_card("Total Views", f"{total_views:,}", "👁️")
with col3:
    metric_card("Likes", f"{total_likes:,}", "🔥")
with col4:
    metric_card("Comments", f"{total_comments:,}", "💬")

# =====================
# TABS
# =====================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview", 
    "📺 Channel Analysis", 
    "🎬 Video Performance", 
    "📅 Daily Trends"
])

# =====================
# TAB 1: Overview
# =====================
with tab1:
    st.subheader("📊 Views Over Time")
    daily = df.groupby("date")[["views"]].sum().reset_index()
    fig = px.line(daily, x="date", y="views", title="Daily Views Trend")
    st.plotly_chart(fig, use_container_width=True)

# =====================
# TAB 2: Channel Analysis
# =====================
with tab2:
    st.subheader("🏆 Channel Comparison")

    ch_views = df.groupby("channel_name")[["views"]].sum().reset_index()
    fig = px.bar(
        ch_views,
        x="channel_name",
        y="views",
        text_auto=True,
        title="Total Views Per Channel"
    )
    st.plotly_chart(fig, use_container_width=True)

# =====================
# TAB 3: Video Performance
# =====================
with tab3:
    st.subheader("🔥 Top Videos by Views")

    top_videos = df.groupby(["video_id","title"])["views"].sum().reset_index()
    top_videos = top_videos.sort_values("views", ascending=False).head(20)

    st.dataframe(top_videos)

# =====================
# TAB 4: Daily Trends
# =====================
with tab4:
    st.subheader("📅 Likes & Comments Over Time")

    daily_stats = df.groupby("date")[["likes","comments"]].sum().reset_index()
    fig = px.line(
        daily_stats,
        x="date",
        y=["likes","comments"],
        title="Daily Likes & Comments"
    )
    st.plotly_chart(fig, use_container_width=True)