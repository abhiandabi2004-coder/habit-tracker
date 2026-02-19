from database import connect_db
import sqlite3

def register_user(name, age, gender, occupation, username, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users(name, age, gender, occupation, username, password)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, age, gender, occupation, username, password))
        conn.commit()
        conn.close()
        return "success"
    except sqlite3.IntegrityError:
        return "duplicate"

def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password),
    )
    user = cursor.fetchone()
    conn.close()
    return user
