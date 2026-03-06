import psycopg2

DATABASE_URL = "postgresql://postgres:HabitTracker@123@db.tzntcjmbtvextrydkjjq.supabase.co:5432/postgres"

def connect_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        occupation TEXT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        habit_name TEXT,
        target_days INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habit_logs (
        id SERIAL PRIMARY KEY,
        habit_id INTEGER REFERENCES habits(id),
        date DATE,
        value INTEGER
    )
    """)

    conn.commit()
    conn.close()
