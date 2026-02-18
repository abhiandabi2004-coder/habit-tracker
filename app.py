import streamlit as st
from database import create_tables
from auth import login_user, register_user
from habit_engine import add_habit, log_habit, get_user_habits
from dashboard import show_dashboard
from pdf_export import generate_pdf_report
import scheduler

st.set_page_config(page_title="Habit Tracker", layout="wide")

create_tables()

st.title("🔥 Habit Tracker Application")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ---------------- AUTH ---------------- #

if choice == "Register":
    st.subheader("Create Account")

    name = st.text_input("Name")
    age = st.number_input("Age", 10, 100)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    occupation = st.text_input("Occupation")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        register_user(name, age, gender, occupation, username, password)
        st.success("Account Created Successfully")

elif choice == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.user_id = user[0]
            st.success("Login Successful")
        else:
            st.error("Invalid Credentials")

# ---------------- MAIN APP ---------------- #

if st.session_state.user_id:

    st.sidebar.success("Logged In")

    app_menu = st.sidebar.radio("Navigate", ["Add Habit", "Track Habit", "Dashboard", "Download Report"])

    if app_menu == "Add Habit":
        habit_name = st.text_input("Habit Name")
        target_days = st.number_input("Target Days", 1, 365)

        if st.button("Add Habit"):
            add_habit(st.session_state.user_id, habit_name, target_days)
            st.success("Habit Added Successfully")

    elif app_menu == "Track Habit":
        habits = get_user_habits(st.session_state.user_id)

        for habit in habits:
            if st.button(f"Mark Complete - {habit[2]}"):
                log_habit(habit[0])
                st.success(f"{habit[2]} Logged")

    elif app_menu == "Dashboard":
        show_dashboard(st.session_state.user_id)

    elif app_menu == "Download Report":
        file_path = generate_pdf_report(st.session_state.user_id)
        with open(file_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="Habit_Report.pdf")