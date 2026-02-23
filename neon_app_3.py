import streamlit as st
import pandas as pd
import plotly.express as px
from db_neon_1 import fetch_df   # Your Neon DB helper

st.set_page_config(page_title="YouTube Intelligence Dashboard", layout="wide")

# =====================
# LOAD DATA FROM NEON
# =====================

@st.cache_data(ttl=600)  # cache for 10 minutes (IMPORTANT)
def load_data():
    video_master = fetch_df("SELECT * FROM video_master")
    stats = fetch_df("SELECT * FROM daily_video_stats")
    channels = fetch_df("SELECT * FROM channels")
    return video_master, stats, channels

video_master, stats, channels = load_data()


# =====================
# MERGE STATS + VIDEO MASTER
# =====================
video_master_clean = video_master.drop(columns=["channel_id", "channel_name"], errors="ignore")
df = stats.merge(video_master_clean, on="video_id", how="left")

df["date"] = pd.to_datetime(df["date"], errors="coerce")

# =====================
# SIDEBAR FILTERS
# =====================
st.sidebar.title("🎯 Filters")

channel_filter = st.sidebar.multiselect(
    "Select Channel",
    channels["channel_name"].unique().tolist(),
    default=channels["channel_name"].unique().tolist()
)

date_range = st.sidebar.date_input(
    "Date Range",
    [df["date"].min(), df["date"].max()]
)

# Apply filters
df = df[df["channel_name"].isin(channel_filter)]
start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

# =====================
# HEADER
# =====================
st.markdown("""
<h1 style='text-align:center; color:#FF4B4B;'>🔥 YouTube Intelligence Dashboard</h1>
""", unsafe_allow_html=True)

# =====================
# KPI CARDS
# =====================
def metric_card(title, value, icon):
    st.markdown(
        f"""
        <div style="background:#1E1E1E; padding:20px; border-radius:15px; text-align:center;
                    color:white; font-size:22px; font-weight:600;">
            <div style="font-size:50px;">{icon}</div>
            {title}<br>
            <span style="font-size:28px; color:#FFD700;">{value}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

col1, col2, col3, col4 = st.columns(4)

with col1: metric_card("Total Videos", f"{df['video_id'].nunique():,}", "🎬")
with col2: metric_card("Total Views", f"{df['views'].sum():,}", "👁️")
with col3: metric_card("Total Likes", f"{df['likes'].sum():,}", "🔥")
with col4: metric_card("Total Comments", f"{df['comments'].sum():,}", "💬")

# =====================
# TABS
# =====================
tab1, tab2, tab3 = st.tabs(["📈 Trends", "⭐ Best Videos", "📺 Channel Analysis"])


# =====================
# TAB 1: TRENDS
# =====================
with tab1:
    # ======================
    # MONTHLY VIEWS (Your code)
    # ======================
    df["month"] = df["published_at"].dt.strftime("%Y-%m")

    monthly = (
        df.groupby("month")
        .agg(
            views=("views", "sum"),
            likes=("likes", "sum"),
            comments=("comments", "sum"),
            published=("published_at", "min")
        )
        .reset_index()
        .sort_values("published")
    )

    st.subheader("🚀 Monthly Views")
    st.plotly_chart(
        px.line(monthly, x="month", y="views", markers=True),
        use_container_width=True
    )

    # ======================
    # ENGAGEMENT RATE TREND
    # ======================
    # Avoid division by zero
    monthly["engagement_rate"] = (
        (monthly["likes"] + monthly["comments"]) / monthly["views"].replace(0, pd.NA)
    ) * 100

    st.subheader("🔥 Engagement Rate Trend (%)")

    fig_er = px.line(
        monthly,
        x="month",
        y="engagement_rate",
        markers=True,
        labels={"engagement_rate": "Engagement Rate (%)", "month": "Month"}
    )

    st.plotly_chart(fig_er, use_container_width=True)

 

# =====================
# TAB 2: BEST VIDEOS
# =====================
with tab2:
    st.subheader("🌟 Top 10 Videos by Views")

    top_views = df.groupby(["video_id", "title"])["views"].sum().reset_index()
    top_views = top_views.sort_values("views", ascending=False).head(10)

    fig2 = px.bar(top_views, x="title", y="views", title="Top 10 Videos by Views")
    st.plotly_chart(fig2, use_container_width=True)


# =====================
# TAB 3: CHANNEL ANALYSIS
# =====================
with tab3:
    st.subheader("📊 Channel Share by Views")

    channel_views = df.groupby("channel_name")["views"].sum().reset_index()

    fig3 = px.pie(channel_views, names="channel_name", values="views",
                  title="Channel Comparison by Views")
    st.plotly_chart(fig3, use_container_width=True)

