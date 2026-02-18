import sqlite3
from database import connect_db

def register_user(name, age, gender, occupation, username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO users(name, age, gender, occupation, username, password)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, age, gender, occupation, username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user