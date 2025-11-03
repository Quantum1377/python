import sqlite3

def connect():
    conn = sqlite3.connect("system.db")
    c = conn.cursor()

    # Tabela de usuários
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        balance REAL DEFAULT 10000
    )
    """)

    # Tabela de ativos
    c.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL
    )
    """)

    # Tabela de transações
    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        asset_id INTEGER,
        quantity REAL,
        total REAL,
        type TEXT,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(asset_id) REFERENCES assets(id)
    )
    """)

    # Inserir ativos iniciais se não existirem
    c.execute("SELECT COUNT(*) FROM assets")
    if c.fetchone()[0] == 0:
        assets = [
            ("Bitcoin", 30000),
            ("Ethereum", 2000),
            ("Dogecoin", 0.15)
        ]
        c.executemany("INSERT INTO assets (name, price) VALUES (?, ?)", assets)

    conn.commit()
    conn.close()
