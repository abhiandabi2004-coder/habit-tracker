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

    if df.empty:
        st.info("No activity logged yet.")
        return

    df["date"] = pd.to_datetime(df["date"])

    # ---------------- STUDY HABITS ---------------- #

    study_df = df[df["habit_name"].str.lower().str.contains("study")]

    if not study_df.empty:
        st.subheader("📚 Study Hours Progress")

        fig1 = px.line(
            study_df,
            x="date",
            y="value",
            color="habit_name",
            markers=True,
        )
        st.plotly_chart(fig1)

    # ---------------- OTHER HABITS ---------------- #

    other_df = df[~df["habit_name"].str.lower().str.contains("study")]

    if not other_df.empty:
        st.subheader("✅ Habit Completion Count")

        summary = other_df.groupby("habit_name")["value"].sum().reset_index()

        fig2 = px.bar(
            summary,
            x="habit_name",
            y="value",
            color="habit_name",
        )
        st.plotly_chart(fig2)

    # ---------------- STREAK ---------------- #

    st.subheader("🔥 Streaks")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, habit_name FROM habits WHERE user_id=?", (user_id,))
    habits = cursor.fetchall()
    conn.close()

    for habit_id, habit_name in habits:
        streak = calculate_streak(habit_id)
        st.write(f"{habit_name}: {streak} days")
