# import_to_neon.py
import pandas as pd
from db import execute_query

# Define CSV files and table info
tables = {
    "channels": {
        "file": "channels.csv",
        "columns": ["channel_id", "channel_name"],
        "query": """
            INSERT INTO channels (channel_id, channel_name)
            VALUES (%s, %s, %s)
            ON CONFLICT (channel_name) DO NOTHING
        """
    },
    "video_master": {
        "file": "video_master.csv",
        "columns": ["published_at", "video_id", "title", "channel_id", "channel_name"],
        "query": """
            INSERT INTO video_master (published_at, video_id, title, channel_id, channel_name)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (video_id) DO NOTHING
        """
    },
    "video_daily_stats": {
        "file": "video_daily_stats.csv",
        "columns": ["likes", "views", "date", "comments", "video_id", "channel_name", "channel_id"],
        "query": """
            INSERT INTO video_daily_stats (likes, views, date, comments, video_id, channel_name, channel_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (video_id, date) DO NOTHING
        """
    }
}

# Function to import a single table
def import_table(table_info):
    df = pd.read_csv(table_info["file"], encoding="utf-8")
    print(f"Importing {table_info['file']} ({len(df)} rows)...")
    
    for _, row in df.iterrows():
        values = tuple(row[col] for col in table_info["columns"])
        success = execute_query(table_info["query"], values)
        if not success:
            print(f"Skipped row due to error: {values}")
    
    print(f"Finished importing {table_info['file']}.\n")

# Import all tables
for table_name, info in tables.items():
    import_table(info)

print("All tables imported successfully!")