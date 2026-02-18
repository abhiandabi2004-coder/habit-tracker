import streamlit as st
import pandas as pd
import plotly.express as px
from database import connect_db
from habit_engine import calculate_streak

def show_dashboard(user_id):
    conn = connect_db()
    df = pd.read_sql("""
    SELECT habits.habit_name, habit_logs.date
    FROM habit_logs
    JOIN habits ON habits.id = habit_logs.habit_id
    WHERE habits.user_id=?
    """, conn, params=(user_id,))

    if df.empty:
        st.warning("No Data Available")
        return

    st.subheader("Habit Progress Over Time")

    df['date'] = pd.to_datetime(df['date'])
    df_group = df.groupby(['date']).size().reset_index(name='count')

    fig = px.line(df_group, x="date", y="count", title="Daily Habit Completion")
    st.plotly_chart(fig)

    st.subheader("🔥 Streaks")
    habits = df['habit_name'].unique()

    for habit in habits:
        habit_id = pd.read_sql("SELECT id FROM habits WHERE habit_name=?", conn, params=(habit,)).iloc[0][0]
        streak = calculate_streak(habit_id)
        st.write(f"{habit}: {streak} Days")