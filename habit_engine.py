import sqlite3
from datetime import datetime, timedelta
from database import connect_db

def add_habit(user_id, habit_name, target_days):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO habits(user_id, habit_name, target_days)
        VALUES (?, ?, ?)
    """, (user_id, habit_name, target_days))

    conn.commit()
    conn.close()

def get_user_habits(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM habits WHERE user_id=?", (user_id,))
    habits = cursor.fetchall()

    conn.close()
    return habits

def log_habit(habit_id):
    conn = connect_db()
    cursor = conn.cursor()

    today = datetime.today().strftime("%Y-%m-%d")

    # Prevent duplicate logging for same day
    cursor.execute("""
        SELECT * FROM habit_logs
        WHERE habit_id=? AND date=?
    """, (habit_id, today))

    existing = cursor.fetchone()

    if not existing:
        cursor.execute("""
            INSERT INTO habit_logs(habit_id, date)
            VALUES (?, ?)
        """, (habit_id, today))
        conn.commit()

    conn.close()

def calculate_streak(habit_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date FROM habit_logs
        WHERE habit_id=?
        ORDER BY date DESC
    """, (habit_id,))

    dates = cursor.fetchall()
    conn.close()

    if not dates:
        return 0

    streak = 0
    today = datetime.today().date()

    for i, date_tuple in enumerate(dates):
        log_date = datetime.strptime(date_tuple[0], "%Y-%m-%d").date()

        if log_date == today - timedelta(days=i):
            streak += 1
        else:
            break

    return streak
