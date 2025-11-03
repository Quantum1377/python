import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# Conecta no banco
conn = sqlite3.connect("system.db")
c = conn.cursor()

st.title("Dashboard de Login de Usuários")

# --- Funções ---
def get_current_sessions():
    c.execute("""
        SELECT users.username, sessions.login_time 
        FROM sessions 
        JOIN users ON users.id = sessions.user_id
        WHERE sessions.logout_time IS NULL
    """)
    return c.fetchall()

def get_last_hour_logins():
    one_hour_ago = datetime.now() - timedelta(hours=1)
    c.execute("""
        SELECT users.username, sessions.login_time, sessions.logout_time
        FROM sessions
        JOIN users ON users.id = sessions.user_id
        WHERE sessions.login_time >= ?
    """, (one_hour_ago.strftime("%Y-%m-%d %H:%M:%S"),))
    return c.fetchall()

def get_all_sessions():
    c.execute("""
        SELECT users.username, sessions.login_time, sessions.logout_time
        FROM sessions
        JOIN users ON users.id = sessions.user_id
    """)
    return c.fetchall()

# --- Sessões ativas ---
st.subheader("Usuários logados atualmente")
current_sessions = get_current_sessions()
st.write(f"Total de usuários logados: {len(current_sessions)}")
for u, login_time in current_sessions:
    st.write(f"- {u}, logado desde {login_time}")

# --- Última hora ---
st.subheader("Usuários que logaram na última hora")
last_hour_sessions = get_last_hour_logins()
st.write(f"Total de logins na última hora: {len(last_hour_sessions)}")
for u, login_time, logout_time in last_hour_sessions:
    status = "Ativo" if logout_time is None else f"Deslogado às {logout_time}"
    st.write(f"- {u}, login: {login_time}, status: {status}")

# --- Histórico completo ---
st.subheader("Histórico de todas as sessões")
all_sessions = get_all_sessions()
for u, login_time, logout_time in all_sessions:
    duration = "Ativo" if logout_time is None else str(datetime.strptime(logout_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(login_time, "%Y-%m-%d %H:%M:%S"))
    st.write(f"- {u}, login: {login_time}, logout: {logout_time}, duração: {duration}")
