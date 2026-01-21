import psycopg
from db_config import DB_CONFIG
from datetime import datetime
from psycopg.types.json import Json



def insert_log(level, service, message, context, user_id):
    """
    Sparar en ny logg kopplad till en användare.
    """
    sql = """
        INSERT INTO logs (timestamp, level, service, message, context, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    datetime.utcnow(),
                    level,
                    service,
                    message,
                    Json(context),
                    user_id,
                ),
            )
        conn.commit()
