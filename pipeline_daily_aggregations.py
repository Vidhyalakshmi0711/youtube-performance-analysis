from db_neon_1 import execute_query

# ---------------------------------------------------------
# DAILY CHANNEL STATS
# ---------------------------------------------------------
def update_daily_channel_stats():
    execute_query("""
        INSERT INTO daily_channel_stats (date, channel_name, views, likes, comments)
        SELECT 
            date,
            channel_name,
            SUM(views),
            SUM(likes),
            SUM(comments)
        FROM video_daily_stats
        WHERE date = CURRENT_DATE
        GROUP BY date, channel_name
        ON CONFLICT (date, channel_name)
        DO UPDATE SET 
            views = EXCLUDED.views,
            likes = EXCLUDED.likes,
            comments = EXCLUDED.comments;
    """)

# ---------------------------------------------------------
# DAILY VIDEO STATS
# ---------------------------------------------------------
def update_daily_video_stats():
    execute_query("""
        INSERT INTO daily_video_stats (date, channel_name, video_id, views, likes, comments)
        SELECT 
            date,
            channel_name,
            video_id,
            views,
            likes,
            comments
        FROM video_daily_stats
        WHERE date = CURRENT_DATE
        ON CONFLICT (date, video_id)
        DO UPDATE SET 
            views = EXCLUDED.views,
            likes = EXCLUDED.likes,
            comments = EXCLUDED.comments;
    """)

# ---------------------------------------------------------
# DAILY TOTAL VIEWS
# ---------------------------------------------------------
def update_daily_views_mv():
    execute_query("""
        INSERT INTO daily_views_mv (date, total_views)
        SELECT 
            CURRENT_DATE,
            SUM(views)
        FROM video_daily_stats
        WHERE date = CURRENT_DATE
        ON CONFLICT (date)
        DO UPDATE SET 
            total_views = EXCLUDED.total_views;
    """)

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def run_all():
    update_daily_channel_stats()
    update_daily_video_stats()
    update_daily_views_mv()
    print("✅ Aggregations Done.")

if __name__ == "__main__":

    run_all()
