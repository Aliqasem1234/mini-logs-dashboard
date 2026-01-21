import psycopg
import pandas as pd
from db_config import DB_CONFIG


def hamta_loggar(user_id, role, sida=1, antal_per_sida=50):
    """
    Hämtar loggar:
    - admin: alla loggar
    - user: endast egna loggar
    """
    offset = (sida - 1) * antal_per_sida

    if role == "admin":
        sql = """
            SELECT id, timestamp, level, service, message, context
            FROM logs
            ORDER BY timestamp DESC
            LIMIT %s OFFSET %s
        """
        params = (antal_per_sida, offset)
    else:
        sql = """
            SELECT id, timestamp, level, service, message, context
            FROM logs
            WHERE user_id = %s
            ORDER BY timestamp DESC
            LIMIT %s OFFSET %s
        """
        params = (user_id, antal_per_sida, offset)

    with psycopg.connect(**DB_CONFIG) as conn:
        df = pd.read_sql_query(sql, conn, params=params)

    return df
