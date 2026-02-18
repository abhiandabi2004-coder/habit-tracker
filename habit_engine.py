import sqlite3
from database import connect_db
from datetime import datetime, timedelta

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
    cursor.execute("INSERT INTO habit_logs(habit_id, date) VALUES (?, ?)", (habit_id, today))
    conn.commit()
    conn.close()

def calculate_streak(habit_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT date FROM habit_logs WHERE habit_id=? ORDER BY date DESC", (habit_id,))
    dates = cursor.fetchall()

    streak = 0
    today = datetime.today()

    for i, date in enumerate(dates):
        log_date = datetime.strptime(date[0], "%Y-%m-%d")
        if log_date.date() == (today - timedelta(days=i)).date():
            streak += 1
        else:
            break

    conn.close()
    return streak