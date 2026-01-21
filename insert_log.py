# insert_log.py
import psycopg
from db_config import DB_CONFIG
import json

def insert_log(level: str, service: str, message: str, context=None):
    if context is None:
        context = {}
    sql = """
        INSERT INTO logs (level, service, message, context)
        VALUES (%s, %s, %s, %s)
    """
    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (level, service, message, json.dumps(context)))
            conn.commit()
        print("✅ Logg infogad")
    except Exception as e:
        print("❌ Misslyckades:", e)