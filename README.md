📊 Media Company YouTube Analytics Dashboard

A professional end-to-end YouTube analytics data pipeline and interactive dashboard built using:

YouTube Data API

PostgreSQL

Python ETL pipelines (incremental & quota-optimized)

Streamlit Professional Dashboard

This project is designed for media companies, data analysts, and ML engineers to monitor channel and video performance at scale.

🚀 Architecture Overview

YouTube API → Python ETL Pipeline → PostgreSQL → Streamlit Dashboard

| Layer       | Technology       | Purpose                                |
| ----------- | ---------------- | -------------------------------------- |
| Data Source | YouTube Data API | Fetch videos & statistics              |
| Storage     | PostgreSQL       | Central analytics database             |
| ETL         | Python           | Incremental fetch & quota optimization |
| Dashboard   | Streamlit        | Interactive BI dashboard               |


🧠 Features
✅ Data Pipeline

Incremental video fetch (only new videos)

Daily statistics tracking

Pagination for 1000+ videos

Quota-optimized API calls

Multi-channel support

✅ PostgreSQL Analytics Tables

channels

video_master

video_daily_stats

✅ Professional Dashboard

KPI Metrics (Views, Likes, Comments, Videos)

Tabs:

Overview

Channel Analysis

Video Performance

Daily Trends

Date & Channel Filters

Interactive Plotly charts
