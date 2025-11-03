import sqlite3
from datetime import datetime

def connect():
    conn = sqlite3.connect("system.db")
    c = conn.cursor()

    # Produtos
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        stock INTEGER,
        price REAL,
        date_added TEXT
    )
    """)

    # Vendas
    c.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER,
        sale_time TEXT,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)

    # Inserir alguns produtos iniciais se não existirem
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        produtos = [
            ("SD Card 64GB", "Storage", 20, 50, datetime.now().strftime("%Y-%m-%d")),
            ("SSD 240GB", "Storage", 10, 200, datetime.now().strftime("%Y-%m-%d")),
            ("Mouse Gamer", "Periféricos", 15, 120, datetime.now().strftime("%Y-%m-%d")),
            ("Teclado Mecânico", "Periféricos", 8, 350, datetime.now().strftime("%Y-%m-%d"))
        ]
        c.executemany("INSERT INTO products (name, category, stock, price, date_added) VALUES (?, ?, ?, ?, ?)", produtos)
    
    conn.commit()
    conn.close()
