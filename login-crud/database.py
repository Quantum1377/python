import sqlite3

def connect():
    conn = sqlite3.connect("system.db")
    c = conn.cursor()

    # Cria tabela de usuários
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Cria tabela de produtos
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL,
        stock INTEGER
    )
    """)

    conn.commit()
    conn.close()
