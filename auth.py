# auth.py
import hashlib
from fetch_logs import DB_CONFIG
import psycopg

def hash_pwd(p: str) -> str:
    """Returnera SHA-256 hash för lösenord."""
    return hashlib.sha256(p.encode()).hexdigest()

def verify_user(username: str, password: str):
    """Verifiera användare mot databasen."""
    password = password[:72]          # säkerställa maxlängd
    sql = "SELECT password_hash, role FROM users WHERE username = %s"
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (username,))
            row = cur.fetchone()
            if not row:
                return None
            hash_db, role = row
            if hash_pwd(password) == hash_db:
                return role
    return None