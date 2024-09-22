import hashlib
import sqlite3
from contextlib import contextmanager

DATABASE_NAME = "users.db"


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS users
                 (email TEXT PRIMARY KEY, name TEXT, password TEXT)"""
        )
        conn.commit()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(email, name, password):
    hashed_password = hash_password(password)
    with get_db_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (email, name, password) VALUES (?, ?, ?)", (email, name, hashed_password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def authenticate_user(email, password):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE email = ?", (email,))
        result = c.fetchone()
        if result:
            stored_password = result[0]
            return stored_password == hash_password(password)
    return False
