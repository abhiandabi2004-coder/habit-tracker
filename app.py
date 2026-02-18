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

# ---------------- AUTH ---------------- #

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
        ["Add Habits", "Track Habits", "Dashboard", "Download Report", "Logout"]
    )

    # ---------------- ADD MULTIPLE HABITS ---------------- #

    if app_menu == "Add Habits":

        st.subheader("➕ Add Multiple Habits")

        num_habits = st.number_input(
            "How many habits do you want to add?",
            min_value=1,
            max_value=20,
            step=1
        )

        habit_names = []

        for i in range(int(num_habits)):
            habit = st.text_input(f"Enter Habit {i+1}", key=f"habit_input_{i}")
            habit_names.append(habit)

        if st.button("Save Habits"):
            for habit in habit_names:
                if habit.strip() != "":
                    add_habit(st.session_state.user_id, habit, 30)
            st.success("Habits Added Successfully!")
            st.rerun()

        # Show existing habits
        st.subheader("📋 Your Habit List")
        habits = get_user_habits(st.session_state.user_id)

        if habits:
            for i, habit in enumerate(habits, start=1):
                st.write(f"Habit {i}: {habit[2]}")
        else:
            st.info("No habits added yet.")

    # ---------------- TRACK HABITS WITH CHECKBOX ---------------- #

    elif app_menu == "Track Habits":

        st.subheader("✅ Complete Today's Habits")

        habits = get_user_habits(st.session_state.user_id)

        if not habits:
            st.warning("Add habits first.")
        else:
            selected_habits = []

            for habit in habits:
                checked = st.checkbox(
                    habit[2],
                    key=f"check_{habit[0]}"
                )
                if checked:
                    selected_habits.append(habit)

            if st.button("Submit Today's Progress"):
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
