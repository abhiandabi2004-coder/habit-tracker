from datetime import datetime, timedelta
from database import connect_db


def add_habit(user_id, habit_name, target_days):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO habits(user_id, habit_name, target_days) VALUES (?, ?, ?)",
        (user_id, habit_name, target_days),
    )
    conn.commit()
    conn.close()


def get_user_habits(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits WHERE user_id=?", (user_id,))
    habits = cursor.fetchall()
    conn.close()
    return habits


def update_habit(habit_id, new_name, new_target):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE habits SET habit_name=?, target_days=? WHERE id=?",
        (new_name, new_target, habit_id),
    )
    conn.commit()
    conn.close()


def delete_habit(habit_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habits WHERE id=?", (habit_id,))
    conn.commit()
    conn.close()


def log_habit(habit_id, value):
    conn = connect_db()
    cursor = conn.cursor()

    today = datetime.now().date().isoformat()

    cursor.execute(
        "SELECT 1 FROM habit_logs WHERE habit_id=? AND date=?",
        (habit_id, today),
    )

    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO habit_logs(habit_id, date, value) VALUES (?, ?, ?)",
            (habit_id, today, value),
        )
        conn.commit()

    conn.close()


def calculate_streak(habit_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT date FROM habit_logs WHERE habit_id=? ORDER BY date DESC",
        (habit_id,),
    )

    dates = cursor.fetchall()
    conn.close()

    if not dates:
        return 0

    dates = [datetime.strptime(d[0], "%Y-%m-%d").date() for d in dates]

    today = datetime.now().date()
    streak = 0
    current_day = today

    for d in dates:
        if d == current_day:
            streak += 1
            current_day -= timedelta(days=1)
        else:
            break

    return streak
