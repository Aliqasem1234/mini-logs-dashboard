import psycopg
from db_config import DB_CONFIG
import pandas as pd

# ─────────────────────────────────────────────
# Hämtar loggar från databasen med pagination
# ─────────────────────────────────────────────
def hamta_loggar(sida: int = 1, antal_per_sida: int = 50, level_filter: str = None):
    offset = (sida - 1) * antal_per_sida

    if level_filter:
        sql = """
            SELECT id, timestamp, level, service, message, context
            FROM logs
            WHERE level = %s
            ORDER BY timestamp DESC
            LIMIT %s OFFSET %s
        """
        params = (level_filter, antal_per_sida, offset)
    else:
        sql = """
            SELECT id, timestamp, level, service, message, context
            FROM logs
            ORDER BY timestamp DESC
            LIMIT %s OFFSET %s
        """
        params = (antal_per_sida, offset)

    # Kör SQL-frågan och returnera som DataFrame
    with psycopg.connect(**DB_CONFIG) as conn:
        df = pd.read_sql_query(sql, conn, params=params)

    return df

# ─────────────────────────────────────────────
# Räknar totalt antal loggar (med valfritt filter)
# ─────────────────────────────────────────────
def rakna_loggar(level_filter: str = None):
    if level_filter:
        sql = "SELECT COUNT(*) FROM logs WHERE level = %s"
        params = (level_filter,)
    else:
        sql = "SELECT COUNT(*) FROM logs"
        params = ()

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()[0]
