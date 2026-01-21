import hashlib
import psycopg
from db_config import DB_CONFIG


def hash_pwd(password: str) -> str:
    """Returnerar SHA-256-hash för lösenord."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_user(username: str, password: str):
    """
    Verifierar användare.
    Returnerar (user_id, role) vid korrekt inloggning.
    """
    sql = """
        SELECT id, password_hash, role
        FROM users
        WHERE username = %s
    """

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (username,))
            row = cur.fetchone()

            if not row:
                return None

            user_id, hash_db, role = row

            if hash_pwd(password) == hash_db:
                return user_id, role

    return None
