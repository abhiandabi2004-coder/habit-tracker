import sqlite3
from datetime import datetime, timedelta
from database import connect_db


# ---------------- ADD HABIT ---------------- #

def add_habit(user_id, habit_name, target_days):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO habits(user_id, habit_name, target_days)
        VALUES (?, ?, ?)
    """, (user_id, habit_name, target_days))

    conn.commit()
    conn.close()


# ---------------- GET USER HABITS ---------------- #

def get_user_habits(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, user_id, habit_name, target_days
        FROM habits
        WHERE user_id=?
    """, (user_id,))

    habits = cursor.fetchall()
    conn.close()

    return habits


# ---------------- LOG HABIT (NO DUPLICATE PER DAY) ---------------- #

def log_habit(habit_id):
    conn = connect_db()
    cursor = conn.cursor()

    today = datetime.now().date().isoformat()

    # Check if already logged today
    cursor.execute("""
        SELECT 1 FROM habit_logs
        WHERE habit_id=? AND date=?
    """, (habit_id, today))

    already_logged = cursor.fetchone()

    if not already_logged:
        cursor.execute("""
            INSERT INTO habit_logs(habit_id, date)
            VALUES (?, ?)
        """, (habit_id, today))
        conn.commit()

    conn.close()


# ---------------- CALCULATE STREAK ---------------- #

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

    # Convert string dates to date objects
    dates = [datetime.strptime(d[0], "%Y-%m-%d").date() for d in dates]

    today = datetime.now().date()
    streak = 0
    current_day = today

    for log_date in dates:
        if log_date == current_day:
            streak += 1
            current_day = current_day - timedelta(days=1)
        else:
            break

    return streak
