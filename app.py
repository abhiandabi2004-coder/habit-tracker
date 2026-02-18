import streamlit as st
from database import create_tables
from auth import login_user, register_user
from habit_engine import add_habit, log_habit, get_user_habits
from dashboard import show_dashboard
from pdf_export import generate_pdf_report

st.set_page_config(page_title="Habit Tracker", layout="wide")

create_tables()

st.title("🔥 Habit Tracker Application")

# ---------------- SESSION ---------------- #

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ---------------- AUTH MENU ---------------- #

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
            register_user(name, age, gender, occupation, username, password)
            st.success("Account Created Successfully")

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

# ---------------- MAIN APP ---------------- #

if st.session_state.user_id:

    st.sidebar.success("Logged In")

    app_menu = st.sidebar.radio(
        "Navigate",
        ["Add Habit", "Track Habit", "Dashboard", "Download Report", "Logout"]
    )

    # ---------------- ADD HABIT ---------------- #

    if app_menu == "Add Habit":
        st.subheader("➕ Add New Habit")

        with st.form("habit_form"):
            habit_name = st.text_input("Habit Name")
            target_days = st.number_input("Target Days", 1, 365)

            submit_habit = st.form_submit_button("Add Habit")

            if submit_habit:
                if habit_name.strip() != "":
                    add_habit(st.session_state.user_id, habit_name, target_days)
                    st.success("Habit Added Successfully")
                    st.rerun()
                else:
                    st.warning("Habit name cannot be empty")

        # Show existing habits
        st.subheader("📋 Your Habits")
        habits = get_user_habits(st.session_state.user_id)

        if habits:
            for habit in habits:
                st.write(f"• {habit[2]} (Target: {habit[3]} days)")
        else:
            st.info("No habits added yet.")

    # ---------------- TRACK HABIT ---------------- #

    elif app_menu == "Track Habit":
        st.subheader("✅ Track Today's Habits")

        habits = get_user_habits(st.session_state.user_id)

        if not habits:
            st.warning("Add habits first.")
        else:
            for habit in habits:
                if st.button(
                    f"Mark Complete - {habit[2]}",
                    key=f"log_{habit[0]}"
                ):
                    log_habit(habit[0])
                    st.success(f"{habit[2]} Logged Successfully")
                    st.rerun()

    # ---------------- DASHBOARD ---------------- #

    elif app_menu == "Dashboard":
        show_dashboard(st.session_state.user_id)

    # ---------------- DOWNLOAD REPORT ---------------- #

    elif app_menu == "Download Report":
        st.subheader("📄 Download Progress Report")

        file_path = generate_pdf_report(st.session_state.user_id)

        with open(file_path, "rb") as f:
            st.download_button(
                "Download PDF",
                f,
                file_name="Habit_Report.pdf"
            )

    # ---------------- LOGOUT ---------------- #

    elif app_menu == "Logout":
        st.session_state.user_id = None
        st.success("Logged Out Successfully")
        st.rerun()
