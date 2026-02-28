from googleapiclient.discovery import build
from datetime import datetime
from config import API_KEY
from db_neon_1 import fetch_all, execute_query

youtube = build("youtube", "v3", developerKey=API_KEY)

# --------------------------------------------------------
# GET CHANNELS
# --------------------------------------------------------
def get_channels():
    rows = fetch_all("SELECT channel_id FROM channels")
    return [r[0] for r in rows]

# --------------------------------------------------------
# GET CHANNEL NAME
# --------------------------------------------------------
def get_channel_name(channel_id):
    rows = fetch_all(
        "SELECT channel_name FROM channels WHERE channel_id=%s",
        (channel_id,)
    )
    return rows[0][0] if rows else None

# --------------------------------------------------------
# GET LAST PUBLISHED DATE
# --------------------------------------------------------
def get_last_published_date(channel_id):
    rows = fetch_all(
        "SELECT MAX(published_at) FROM video_master WHERE channel_id=%s",
        (channel_id,)
    )
    return rows[0][0] if rows else None

# --------------------------------------------------------
# INSERT VIDEO
# --------------------------------------------------------
def insert_video(video_id, title, published, channel_id):
    channel_name = get_channel_name(channel_id)

    execute_query("""
        INSERT INTO video_master(video_id, title, published_at, channel_id, channel_name)
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT (video_id) DO NOTHING
    """, (video_id, title, published, channel_id, channel_name))

# --------------------------------------------------------
# FETCH INCREMENTAL VIDEOS
# --------------------------------------------------------
def fetch_incremental_videos(channel_id):
    last_date = get_last_published_date(channel_id)

    if last_date:
        published_after = last_date.isoformat("T") + "Z"
    else:
        published_after = "2000-01-01T00:00:00Z"

    print(f"\n🔹 Fetching new videos for {channel_id} after {published_after}")

    next_page = None
    total_new = 0

    while True:
        response = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="date",
            maxResults=50,
            publishedAfter=published_after,
            pageToken=next_page,
            type="video",
        ).execute()

        for item in response.get("items", []):
            vid = item["id"]["videoId"]
            title = item["snippet"]["title"]
            published = item["snippet"]["publishedAt"]

            insert_video(vid, title, published, channel_id)
            total_new += 1
            print(f"🆕 New video saved: {vid}")

        next_page = response.get("nextPageToken")
        if not next_page:
            break

    print(f"✅ Total NEW videos added for {channel_id}: {total_new}")

# --------------------------------------------------------
# MAIN
# --------------------------------------------------------
def main():
    channels = get_channels()
    for cid in channels:
        fetch_incremental_videos(cid)

if __name__ == "__main__":

    main()
