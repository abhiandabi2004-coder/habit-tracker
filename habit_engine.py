from database import connect_db
from datetime import date


def add_habit(user_id, habit_name, target_days):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO habits(user_id, habit_name, target_days)
        VALUES (%s, %s, %s)
        """,
        (user_id, habit_name, target_days),
    )

    conn.commit()
    conn.close()


def get_habits(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM habits WHERE user_id=%s
        """,
        (user_id,),
    )

    habits = cursor.fetchall()

    conn.close()
    return habits


def mark_complete(habit_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO habit_logs(habit_id, date, value)
        VALUES (%s, %s, %s)
        """,
        (habit_id, date.today(), 1),
    )

    conn.commit()
    conn.close()


def get_streak(habit_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) FROM habit_logs
        WHERE habit_id=%s
        """,
        (habit_id,),
    )

    streak = cursor.fetchone()[0]

    conn.close()
    return streak


def get_progress(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT habit_name, COUNT(habit_logs.id)
        FROM habits
        LEFT JOIN habit_logs
        ON habits.id = habit_logs.habit_id
        WHERE habits.user_id=%s
        GROUP BY habit_name
        """,
        (user_id,),
    )

    data = cursor.fetchall()

    conn.close()
    return data
