import sqlite3

DB_NAME = "habits.db"

def connect_db():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        occupation TEXT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # HABITS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        habit_name TEXT,
        target_days INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # HABIT LOGS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        date TEXT,
        FOREIGN KEY (habit_id) REFERENCES habits(id)
    )
    """)

    conn.commit()
    conn.close()
