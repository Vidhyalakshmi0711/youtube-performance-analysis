from googleapiclient.discovery import build
from datetime import date
from config import API_KEY
from db import fetch_all, execute_query

youtube = build("youtube", "v3", developerKey=API_KEY)

# --------------------------------------------------------
# GET ALL VIDEOS
# --------------------------------------------------------
def get_videos():
    rows = fetch_all("SELECT video_id, channel_id FROM video_master")
    return [(r[0], r[1]) for r in rows]

# --------------------------------------------------------
# LOAD CHANNEL NAMES (one-time lookup)
# --------------------------------------------------------
def load_channel_names():
    rows = fetch_all("SELECT channel_id, channel_name FROM channels")
    return {cid: cname for cid, cname in rows}

# --------------------------------------------------------
# TODAY'S EXISTING STAT RECORDS
# --------------------------------------------------------
def fetch_today_stat_ids():
    rows = fetch_all(
        "SELECT video_id FROM video_daily_stats WHERE date=%s",
        (date.today(),)
    )
    return {r[0] for r in rows}

# --------------------------------------------------------
# INSERT DAILY STATS
# --------------------------------------------------------
def insert_stats(video_id, channel_id, channel_name, views, likes, comments):
    execute_query("""
        INSERT INTO video_daily_stats(video_id, channel_id, channel_name, date, views, likes, comments)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (video_id, date) DO NOTHING
    """, (video_id, channel_id, channel_name, date.today(), views, likes, comments))

# --------------------------------------------------------
# MAIN FETCH LOOP
# --------------------------------------------------------
def fetch_today_stats():

    videos = get_videos()
    todays_stats = fetch_today_stat_ids()
    channel_map = load_channel_names()

    total_new = 0
    total_skipped = 0

    for i in range(0, len(videos), 50):
        batch = videos[i:i+50]

        batch_to_fetch = [(vid, cid) for (vid, cid) in batch if vid not in todays_stats]

        if not batch_to_fetch:
            continue

        video_ids = ",".join([v[0] for v in batch_to_fetch])

        try:
            result = youtube.videos().list(
                part="statistics",
                id=video_ids
            ).execute()

            for item in result.get("items", []):
                vid = item["id"]
                stats = item["statistics"]
                cid = next(cid for (v, cid) in batch_to_fetch if v == vid)
                cname = channel_map.get(cid)

                insert_stats(
                    vid, cid, cname,
                    int(stats.get("viewCount", 0)),
                    int(stats.get("likeCount", 0)),
                    int(stats.get("commentCount", 0))
                )

                total_new += 1
                print(f"📈 Saved stats: {vid}")

        except Exception as e:
            print("Error batch:", e)

        total_skipped += (len(batch) - len(batch_to_fetch))

    print(f"\n✅ New stats added: {total_new}")
    print(f"⏭️ Skipped today: {total_skipped}")

# --------------------------------------------------------
# RUN
# --------------------------------------------------------
if __name__ == "__main__":
    fetch_today_stats()