
import json
import sys
import psycopg2
from psycopg2.extras import execute_batch
from config.settings import DATABASE_URL

def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE IF EXISTS video_snapshots;
        DROP TABLE IF EXISTS videos;

        CREATE TABLE videos (
            id BIGINT PRIMARY KEY,
            creator_id BIGINT NOT NULL,
            video_created_at TIMESTAMP NOT NULL,
            views_count BIGINT,
            likes_count BIGINT,
            comments_count BIGINT,
            reports_count BIGINT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );

        CREATE TABLE video_snapshots (
            id BIGINT PRIMARY KEY,
            video_id BIGINT REFERENCES videos(id),
            views_count BIGINT,
            likes_count BIGINT,
            comments_count BIGINT,
            reports_count BIGINT,
            delta_views_count BIGINT,
            delta_likes_count BIGINT,
            delta_comments_count BIGINT,
            delta_reports_count BIGINT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        """)
        conn.commit()

def load_data(json_path, conn):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    videos = []
    snapshots = []

    for video in 
        videos.append((
            video['id'],
            video['creator_id'],
            video['video_created_at'],
            video.get('views_count'),
            video.get('likes_count'),
            video.get('comments_count'),
            video.get('reports_count'),
            video.get('created_at'),
            video.get('updated_at')
        ))

        for snap in video.get('snapshots', []):
            snapshots.append((
                snap['id'],
                snap['video_id'],
                snap.get('views_count'),
                snap.get('likes_count'),
                snap.get('comments_count'),
                snap.get('reports_count'),
                snap.get('delta_views_count'),
                snap.get('delta_likes_count'),
                snap.get('delta_comments_count'),
                snap.get('delta_reports_count'),
                snap.get('created_at'),
                snap.get('updated_at')
            ))

    with conn.cursor() as cur:
        execute_batch(cur, """
            INSERT INTO videos (id, creator_id, video_created_at, views_count, likes_count, comments_count, reports_count, created_at, updated_at)
            VALUES (%s, %s, %s, % s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, videos)

        execute_batch(cur, """
            INSERT INTO video_snapshots (
                id, video_id, views_count, likes_count, comments_count, reports_count,
                delta_views_count, delta_likes_count, delta_comments_count, delta_reports_count,
                created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (id) DO NOTHING;
        """, snapshots)

        conn.commit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python load_data.py <path_to_videos.json>")
        sys.exit(1)

    json_file = sys.argv[1]
    conn = psycopg2.connect(DATABASE_URL)
    create_tables(conn)
    load_data(json_file, conn)
    conn.close()
    print("✅ Data loaded successfully!")