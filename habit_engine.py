from database import connect_db
from datetime import date


def add_habit(user_id, habit_name, target_days):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO habits (user_id, habit_name, target_days)
        VALUES (%s, %s, %s)
        """,
        (user_id, habit_name, target_days)
    )

    conn.commit()
    conn.close()


def get_user_habits(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM habits WHERE user_id=%s
        """,
        (user_id,)
    )

    habits = cursor.fetchall()
    conn.close()

    return habits


def update_habit(habit_id, habit_name, target_days):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE habits
        SET habit_name=%s, target_days=%s
        WHERE id=%s
        """,
        (habit_name, target_days, habit_id)
    )

    conn.commit()
    conn.close()


def delete_habit(habit_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM habits WHERE id=%s
        """,
        (habit_id,)
    )

    conn.commit()
    conn.close()


def log_habit(habit_id, value=1):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO habit_logs (habit_id, date, value)
        VALUES (%s, %s, %s)
        """,
        (habit_id, date.today(), value)
    )

    conn.commit()
    conn.close()


def calculate_streak(habit_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM habit_logs
        WHERE habit_id=%s
        """,
        (habit_id,)
    )

    streak = cursor.fetchone()[0]

    conn.close()

    return streak
