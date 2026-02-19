import sqlite3

def connect_db():
    return sqlite3.connect("habits.db", check_same_thread=False)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        occupation TEXT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        habit_name TEXT,
        target_days INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habit_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        date TEXT,
        value INTEGER
    )
    """)

    conn.commit()
    conn.close()
