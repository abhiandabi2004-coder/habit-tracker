import streamlit as st
from database import create_tables
from auth import login_user, register_user
from habit_engine import add_habit, log_habit, get_user_habits
from dashboard import show_dashboard
from pdf_export import generate_pdf_report

# ---------------- CONFIG ---------------- #

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

# ---------------- MAIN APP ---------------- #

if st.session_state.user_id:

    app_menu = st.sidebar.radio(
        "Navigate",
        ["Add Habits", "Track Habits", "Dashboard", "Download Report", "Logout"]
    )

    # ---------------- ADD HABITS ---------------- #

    if app_menu == "Add Habits":

        st.subheader("➕ Add Your Habits")

        num_habits = st.number_input(
            "How many habits do you want to add?",
            min_value=1,
            max_value=20,
            step=1
        )

        with st.form("multi_habit_form"):

            habit_data = []

            for i in range(int(num_habits)):
                habit_name = st.text_input(
                    f"Enter Habit {i+1}",
                    key=f"habit_input_{i}"
                )

                target_days = st.number_input(
                    f"Target Days for Habit {i+1}",
                    min_value=1,
                    max_value=365,
                    value=30,
                    key=f"target_input_{i}"
                )

                habit_data.append((habit_name, target_days))

            submit = st.form_submit_button("Save Habits")

            if submit:
                for habit_name, target_days in habit_data:
                    if habit_name.strip():
                        add_habit(
                            st.session_state.user_id,
                            habit_name,
                            target_days
                        )

                st.success("Habits Added Successfully!")
                st.rerun()

        # Show existing habits
        st.subheader("📋 Your Habit List")

        habits = get_user_habits(st.session_state.user_id)

        if habits:
            for i, habit in enumerate(habits, start=1):
                st.write(f"Habit {i}: {habit[2]} (Target: {habit[3]} days)")
        else:
            st.info("No habits added yet.")

    # ---------------- TRACK HABITS ---------------- #

    elif app_menu == "Track Habits":

        st.subheader("✅ Complete Today's Habits")

        habits = get_user_habits(st.session_state.user_id)

        if not habits:
            st.warning("Add habits first.")
        else:
            with st.form("track_form"):

                selected_habits = []

                for habit in habits:
                    if st.checkbox(
                        habit[2],
                        key=f"check_{habit[0]}"
                    ):
                        selected_habits.append(habit)

                submit = st.form_submit_button("Submit Today's Progress")

                if submit:
                    for habit in selected_habits:
                        log_habit(habit[0])

                    st.success("Habits Logged Successfully!")
                    st.rerun()

    # ---------------- DASHBOARD ---------------- #

    elif app_menu == "Dashboard":
        show_dashboard(st.session_state.user_id)

    # ---------------- DOWNLOAD REPORT ---------------- #

    elif app_menu == "Download Report":
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
