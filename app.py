import streamlit as st
from database import create_tables
from auth import login_user, register_user
from habit_engine import add_habit, log_habit, get_user_habits
from dashboard import show_dashboard
from pdf_export import generate_pdf_report

st.set_page_config(page_title="Habit Tracker", layout="wide")
create_tables()

st.title("🔥 Habit Tracker Application")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- REGISTER ---------------- #

if choice == "Register":
    st.subheader("Create Account")

    with st.form("register_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", 10, 100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        occupation = st.text_input("Occupation")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submit = st.form_submit_button("Register")

        if submit:
            result = register_user(name, age, gender, occupation, username, password)

            if result == "success":
                st.success("Account Created Successfully")
            elif result == "duplicate":
                st.error("Username already exists")

# ---------------- LOGIN ---------------- #

elif choice == "Login":
    st.subheader("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submit = st.form_submit_button("Login")

        if submit:
            user = login_user(username, password)
            if user:
                st.session_state.user_id = user[0]
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

# ---------------- MAIN ---------------- #

if st.session_state.user_id:

    app_menu = st.sidebar.radio(
        "Navigate",
        ["Add Habits", "Track Habits", "Dashboard", "Download Report", "Logout"]
    )

    # ---------------- ADD HABITS ---------------- #

    if app_menu == "Add Habits":

        habit_name = st.text_input("Enter Habit Name")
        target_days = st.number_input("Target Days", 1, 365)

        if st.button("Add Habit"):
            if habit_name.strip():
                add_habit(st.session_state.user_id, habit_name, target_days)
                st.success("Habit Added")
                st.rerun()

        habits = get_user_habits(st.session_state.user_id)

        for habit in habits:
            st.write(f"• {habit[2]} (Target: {habit[3]} days)")

    # ---------------- TRACK HABITS ---------------- #

    elif app_menu == "Track Habits":

        habits = get_user_habits(st.session_state.user_id)

        if not habits:
            st.warning("Add habits first")
        else:
            with st.form("track_form"):
                selected = []

                for habit in habits:
                    if st.checkbox(habit[2], key=f"check_{habit[0]}"):
                        selected.append(habit)

                submit = st.form_submit_button("Submit Today's Progress")

                if submit:
                    for habit in selected:
                        log_habit(habit[0])

                    st.success("Habits Logged")
                    st.rerun()

    elif app_menu == "Dashboard":
        show_dashboard(st.session_state.user_id)

    elif app_menu == "Download Report":
        file_path = generate_pdf_report(st.session_state.user_id)
        with open(file_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="Habit_Report.pdf")

    elif app_menu == "Logout":
        st.session_state.user_id = None
        st.rerun()
