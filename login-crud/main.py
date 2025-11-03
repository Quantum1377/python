import sqlite3
from getpass import getpass
from prettytable import PrettyTable
from database import connect

connect()  # cria banco e tabelas

def register():
    username = input("Escolha um nome de usuário: ")
    password = getpass("Escolha uma senha: ")

    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("✅ Usuário registrado com sucesso!")
    except sqlite3.IntegrityError:
        print("⚠️ Usuário já existe!")
    conn.close()

def login():
    username = input("Usuário: ")
    password = getpass("Senha: ")

    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        print(f"✅ Bem-vindo, {username}!")
        return True
    else:
        print("❌ Usuário ou senha incorretos.")
        return False

def add_product():
    name = input("Nome do produto: ")
    price = float(input("Preço: "))
    stock = int(input("Estoque: "))

    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    conn.commit()
    conn.close()
    print("✅ Produto adicionado!")

def list_products():
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()

    table = PrettyTable()
    table.field_names = ["ID", "Nome", "Preço", "Estoque"]
    for p in products:
        table.add_row(p)
    print(table)

def update_product():
    list_products()
    pid = int(input("ID do produto que deseja atualizar: "))
    price = float(input("Novo preço: "))
    stock = int(input("Novo estoque: "))

    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute("UPDATE products SET price=?, stock=? WHERE id=?", (price, stock, pid))
    conn.commit()
    conn.close()
    print("✅ Produto atualizado!")

def delete_product():
    list_products()
    pid = int(input("ID do produto que deseja deletar: "))

    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    print("✅ Produto deletado!")

def main_menu():
    while True:
        print("\n--- MENU ---")
        print("1. Registrar")
        print("2. Login")
        print("3. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            register()
        elif choice == "2":
            if login():
                product_menu()
        elif choice == "3":
            break
        else:
            print("Opção inválida!")

def product_menu():
    while True:
        print("\n--- PRODUTOS ---")
        print("1. Adicionar produto")
        print("2. Listar produtos")
        print("3. Atualizar produto")
        print("4. Deletar produto")
        print("5. Logout")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            list_products()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main_menu()
