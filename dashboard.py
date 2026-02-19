import streamlit as st
import pandas as pd
import plotly.express as px
from database import connect_db
from habit_engine import calculate_streak


def show_dashboard(user_id):

    st.subheader("📊 Habit Dashboard")

    conn = connect_db()

    # Fetch all habits for the user
    habits_df = pd.read_sql("""
        SELECT id, habit_name
        FROM habits
        WHERE user_id=?
    """, conn, params=(user_id,))

    # Fetch habit logs
    logs_df = pd.read_sql("""
        SELECT habit_id, date
        FROM habit_logs
    """, conn)

    conn.close()

    # ---------------- GRAPH SECTION ---------------- #

    st.subheader("📈 Habit Completion Trend")

    if logs_df.empty:
        st.info("No habit activity yet.")
    else:
        logs_df['date'] = pd.to_datetime(logs_df['date'])

        # Count total habits completed per day
        daily_counts = logs_df.groupby('date').size().reset_index(name='count')

        fig = px.line(
            daily_counts,
            x='date',
            y='count',
            markers=True,
            title="Daily Habit Completion"
        )

        st.plotly_chart(fig)

    # ---------------- STREAK SECTION ---------------- #

    st.subheader("🔥 Streaks")

    if habits_df.empty:
        st.info("No habits added yet.")
        return

    for _, row in habits_df.iterrows():
        habit_id = row['id']
        habit_name = row['habit_name']

        streak = calculate_streak(habit_id)

        st.write(f"{habit_name}: {streak} days")
