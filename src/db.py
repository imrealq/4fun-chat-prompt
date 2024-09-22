import hashlib
import os
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
                 (email TEXT PRIMARY KEY, name TEXT, salt TEXT, password TEXT)"""
        )
        conn.commit()


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return salt, hashed


def add_user(email, name, password):
    salt, hashed_password = hash_password(password)
    with get_db_connection() as conn:
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO users (email, name, salt, password) VALUES (?, ?, ?, ?)",
                (email, name, salt, hashed_password),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def authenticate_user(email, password):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT salt, password FROM users WHERE email = ?", (email,))
        result = c.fetchone()
        if result:
            salt, stored_password = result
            _, hashed_password = hash_password(password, salt)
            return hashed_password == stored_password
    return False
