import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# Conecta no banco
conn = sqlite3.connect("system.db", check_same_thread=False)
c = conn.cursor()

st.title("Dashboard de Vendas e Inventário")

# --- Funções ---
def get_products():
    df = pd.read_sql("SELECT * FROM products", conn)
    return df

def get_sales():
    df = pd.read_sql("SELECT sales.id, products.name, sales.quantity, sales.sale_time FROM sales JOIN products ON sales.product_id = products.id", conn)
    return df

def add_sale(product_id, quantity):
    sale_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO sales (product_id, quantity, sale_time) VALUES (?, ?, ?)", (product_id, quantity, sale_time))
    # Atualiza estoque
    c.execute("UPDATE products SET stock = stock - ? WHERE id=?", (quantity, product_id))
    conn.commit()

# --- Sidebar para registrar venda ---
st.sidebar.header("Registrar venda")
products_df = get_products()
product_options = products_df["name"].tolist()
selected_product = st.sidebar.selectbox("Produto", product_options)
quantity = st.sidebar.number_input("Quantidade", min_value=1, max_value=100, value=1)
if st.sidebar.button("Registrar Venda"):
    pid = products_df[products_df["name"] == selected_product]["id"].values[0]
    stock = products_df[products_df["name"] == selected_product]["stock"].values[0]
    if quantity > stock:
        st.sidebar.error("Estoque insuficiente!")
    else:
        add_sale(pid, quantity)
        st.sidebar.success(f"Venda registrada: {selected_product} x{quantity}")

# --- Tabela de produtos ---
st.subheader("Produtos em estoque")
products_df = get_products()
st.dataframe(products_df[["id", "name", "category", "stock", "price"]])

# --- Vendas últimas 24h ---
st.subheader("Vendas últimas 24 horas")
sales_df = get_sales()
last_24h = datetime.now() - timedelta(hours=24)
recent_sales = sales_df[pd.to_datetime(sales_df["sale_time"]) >= last_24h]
st.dataframe(recent_sales)

# --- Gráfico de produtos mais vendidos ---
st.subheader("Produtos mais vendidos")
top_sales = sales_df.groupby("name")["quantity"].sum().reset_index()
fig = px.bar(top_sales, x="name", y="quantity", title="Total vendido por produto")
st.plotly_chart(fig)

# --- Alerta de estoque baixo ---
st.subheader("Produtos com estoque baixo")
low_stock = products_df[products_df["stock"] <= 5]
st.dataframe(low_stock[["name", "stock"]])
