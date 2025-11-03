import sqlite3
import pickle
import numpy as np

DB_NAME = "system.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        encoding BLOB NOT NULL
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS logins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_user(username: str, encoding: np.ndarray):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    enc_blob = pickle.dumps(encoding)
    c.execute("INSERT INTO users (username, encoding) VALUES (?, ?)", (username, enc_blob))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, username, encoding FROM users")
    rows = c.fetchall()
    conn.close()
    users = []
    for row in rows:
        uid, username, enc_blob = row
        encoding = pickle.loads(enc_blob)
        users.append({"id": uid, "username": username, "encoding": encoding})
    return users

def log_login(user_id: int, username: str, timestamp: str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO logins (user_id, username, timestamp) VALUES (?, ?, ?)", (user_id, username, timestamp))
    conn.commit()
    conn.close()
