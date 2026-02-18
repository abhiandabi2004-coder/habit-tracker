import streamlit as st
import pandas as pd
import plotly.express as px
from database import connect_db
from habit_engine import calculate_streak

def show_dashboard(user_id):

    conn = connect_db()

    df = pd.read_sql("""
        SELECT habits.id, habits.habit_name, habit_logs.date
        FROM habits
        LEFT JOIN habit_logs ON habits.id = habit_logs.habit_id
        WHERE habits.user_id=?
    """, conn, params=(user_id,))

    conn.close()

    if df.empty:
        st.warning("No data available.")
        return

    st.subheader("📈 Habit Completion Trend")

    df = df.dropna()

    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        daily_counts = df.groupby('date').size().reset_index(name='count')

        fig = px.line(
            daily_counts,
            x='date',
            y='count',
            markers=True,
            title="Daily Habit Completion"
        )

        st.plotly_chart(fig)

    st.subheader("🔥 Streaks")

    habit_ids = df['id'].unique()

    for habit_id in habit_ids:
        habit_name = df[df['id'] == habit_id]['habit_name'].iloc[0]
        streak = calculate_streak(habit_id)
        st.write(f"{habit_name}: {streak} days")
