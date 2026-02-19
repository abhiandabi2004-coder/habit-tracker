import streamlit as st
import pandas as pd
import plotly.express as px
from database import connect_db
from habit_engine import calculate_streak


def show_dashboard(user_id):

    conn = connect_db()

    df = pd.read_sql(
        """
        SELECT habits.habit_name, habit_logs.date, habit_logs.value
        FROM habit_logs
        JOIN habits ON habits.id = habit_logs.habit_id
        WHERE habits.user_id=?
        """,
        conn,
        params=(user_id,),
    )

    conn.close()

    st.subheader("📈 Habit Performance")

    if df.empty:
        st.info("No activity logged yet.")
    else:
        df["date"] = pd.to_datetime(df["date"])

        fig = px.line(
            df,
            x="date",
            y="value",
            color="habit_name",
            markers=True,
        )

        st.plotly_chart(fig)

    st.subheader("🔥 Streaks")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, habit_name FROM habits WHERE user_id=?", (user_id,))
    habits = cursor.fetchall()
    conn.close()

    for habit_id, habit_name in habits:
        streak = calculate_streak(habit_id)
        st.write(f"{habit_name}: {streak} days")
