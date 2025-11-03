import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import plotly.express as px

# Conexão com banco
conn = sqlite3.connect("system.db", check_same_thread=False)
c = conn.cursor()

st.title("Simulador de Trading / Criptomoedas")

# --- Funções ---
def get_users():
    return pd.read_sql("SELECT * FROM users", conn)

def get_assets():
    return pd.read_sql("SELECT * FROM assets", conn)

def get_transactions():
    return pd.read_sql("""
        SELECT t.id, u.username, a.name as asset, t.quantity, t.total, t.type, t.timestamp
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        JOIN assets a ON t.asset_id = a.id
    """, conn)

def buy_asset(user_id, asset_id, quantity, price):
    total = quantity * price
    c.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    balance = c.fetchone()[0]
    if total > balance:
        return False, "Saldo insuficiente!"
    # Deduz saldo
    c.execute("UPDATE users SET balance = balance - ? WHERE id=?", (total, user_id))
    # Registra transação
    c.execute("INSERT INTO transactions (user_id, asset_id, quantity, total, type, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, asset_id, quantity, total, "BUY", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    return True, "Compra realizada com sucesso!"

def sell_asset(user_id, asset_id, quantity, price):
    # Verifica se usuário possui quantidade suficiente
    df = pd.read_sql("""
        SELECT SUM(CASE WHEN type='BUY' THEN quantity ELSE -quantity END) as qty
        FROM transactions
        WHERE user_id=? AND asset_id=?
    """, conn, params=(user_id, asset_id))
    owned = df['qty'][0] or 0
    if quantity > owned:
        return False, "Você não possui quantidade suficiente!"
    total = quantity * price
    # Adiciona saldo
    c.execute("UPDATE users SET balance = balance + ? WHERE id=?", (total, user_id))
    # Registra transação
    c.execute("INSERT INTO transactions (user_id, asset_id, quantity, total, type, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, asset_id, quantity, total, "SELL", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    return True, "Venda realizada com sucesso!"

# --- Seleção de usuário ---
st.sidebar.header("Usuário")
users_df = get_users()
if users_df.empty:
    st.sidebar.warning("Nenhum usuário cadastrado. Crie um usuário!")
    username = st.sidebar.text_input("Novo usuário")
    if st.sidebar.button("Criar usuário"):
        c.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        st.sidebar.success(f"Usuário {username} criado com saldo inicial de 10.000")
    st.stop()
else:
    username = st.sidebar.selectbox("Selecionar usuário", users_df["username"].tolist())
user_id = users_df[users_df["username"]==username]["id"].values[0]

# --- Seleção de ativo ---
assets_df = get_assets()
asset_name = st.sidebar.selectbox("Ativo", assets_df["name"].tolist())
asset_id = assets_df[assets_df["name"]==asset_name]["id"].values[0]
price = float(assets_df[assets_df["name"]==asset_name]["price"].values[0])
quantity = st.sidebar.number_input("Quantidade", min_value=0.0001, value=1.0, step=0.0001)

# --- Botões de comprar/vender ---
if st.sidebar.button("Comprar"):
    success, msg = buy_asset(user_id, asset_id, quantity, price)
    if success:
        st.sidebar.success(msg)
    else:
        st.sidebar.error(msg)

if st.sidebar.button("Vender"):
    success, msg = sell_asset(user_id, asset_id, quantity, price)
    if success:
        st.sidebar.success(msg)
    else:
        st.sidebar.error(msg)

# --- Dashboard ---
st.subheader(f"Saldo do usuário: {username}")
balance = users_df[users_df["username"]==username]["balance"].values[0]
st.metric("Saldo disponível", f"R$ {balance:.2f}")

st.subheader("Histórico de transações")
transactions_df = get_transactions()
st.dataframe(transactions_df[transactions_df["username"]==username])

st.subheader("Gráfico de ativos comprados")
user_trades = transactions_df[transactions_df["username"]==username].groupby("asset")["quantity"].sum().reset_index()
fig = px.bar(user_trades, x="asset", y="quantity", title="Quantidade total de cada ativo")
st.plotly_chart(fig)
