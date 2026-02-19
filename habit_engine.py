def calculate_streak(habit_id):
    from datetime import datetime, timedelta
    from database import connect_db

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

    dates = [datetime.strptime(d[0], "%Y-%m-%d").date() for d in dates]

    today = datetime.today().date()
    streak = 0
    current_day = today

    for d in dates:
        if d == current_day:
            streak += 1
            current_day = current_day - timedelta(days=1)
        else:
            break

    return streak
