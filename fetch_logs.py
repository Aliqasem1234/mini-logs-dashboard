# fetch_logs.py
import psycopg2 as psycopg
from db_config import DB_CONFIG
import pandas as pd

def hamta_loggar(n: int = 100):
    """
    Hämtar de senaste n loggarna som en DataFrame.
    """
    sql = """
        SELECT id, timestamp, level, service, message, context
        FROM logs
        ORDER BY timestamp DESC
        LIMIT %s
    """
    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            df = pd.read_sql_query(sql, conn, params=(n,))
        return df
    except Exception as e:
        print("❌ Kunde inte hämta loggar:", e)
        return pd.DataFrame()  # tom DataFrame vid fel