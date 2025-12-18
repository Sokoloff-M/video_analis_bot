import psycopg2
from psycopg2.extras import RealDictCursor
from config.settings import DATABASE_URL
from datetime import date

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def execute_scalar(query: str, params: tuple = ()) -> int:
    """Выполняет запрос и возвращает одно число (первое значение первой строки)."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            result = cur.fetchone()
            return result[0] if result and result[0] is not None else 0

def count_all_videos() -> int:
    query = "SELECT COUNT(*) FROM videos;"
    return execute_scalar(query)

def count_videos_by_creator_and_date(creator_id: int, date_from: date, date_to: date) -> int:
    query = """
        SELECT COUNT(*)
        FROM videos
        WHERE creator_id = %s
          AND video_created_at >= %s
          AND video_created_at < %s + INTERVAL '1 day';
    """
    return execute_scalar(query, (creator_id, date_from, date_to))

def count_videos_with_views_gt(threshold: int) -> int:
    query = "SELECT COUNT(*) FROM videos WHERE views_count > %s;"
    return execute_scalar(query, (threshold,))

def sum_delta_views_on_date(target_date: date) -> int:
    query = """
        SELECT COALESCE(SUM(delta_views_count), 0)
        FROM video_snapshots
        WHERE created_at::date = %s;
    """
    return execute_scalar(query, (target_date,))

def count_videos_with_delta_views_on_date(target_date: date) -> int:
    query = """
        SELECT COUNT(DISTINCT video_id)
        FROM video_snapshots
        WHERE delta_views_count > 0
          AND created_at::date = %s;
    """
    return execute_scalar(query, (target_date,))
