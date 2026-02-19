import streamlit as st
from database import create_tables
from auth import register_user, login_user
from habit_engine import (
    add_habit, get_user_habits,
    update_habit, delete_habit,
    log_habit
)
from dashboard import show_dashboard
from pdf_export import generate_pdf_report

create_tables()

st.title("🔥 Habit Tracker App")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ---------------- AUTH ---------------- #

if not st.session_state.user_id:

    menu = st.sidebar.radio("Menu", ["Login", "Register"])

    if menu == "Register":
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
                    st.success("Registered Successfully")
                else:
                    st.error("Username already exists")

    if menu == "Login":
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

    menu = st.sidebar.radio(
        "Navigation",
        ["Add Habits", "Track", "Dashboard", "PDF", "Logout"]
    )

    if menu == "Logout":
        st.session_state.user_id = None
        st.rerun()

    # ---------- ADD HABITS ---------- #

    if menu == "Add Habits":

        num = st.number_input("How many habits do you want to add?", 1, 20)

        with st.form("habit_form"):

            habits_data = []

            for i in range(int(num)):
                name = st.text_input(f"Habit {i+1} Name", key=f"name_{i}")
                target = st.number_input(
                    f"Habit {i+1} Target Days",
                    1,
                    365,
                    key=f"target_{i}"
                )
                habits_data.append((name, target))

            submit = st.form_submit_button("Save Habits")

            if submit:
                for name, target in habits_data:
                    if name.strip():
                        add_habit(st.session_state.user_id, name, target)
                st.success("Habits Added")
                st.rerun()

        habits = get_user_habits(st.session_state.user_id)

        for habit in habits:
            with st.expander(habit[2]):
                new_name = st.text_input(
                    "New Name", value=habit[2], key=f"edit_name_{habit[0]}"
                )
                new_target = st.number_input(
                    "New Target", value=habit[3], key=f"edit_target_{habit[0]}"
                )

                if st.button("Update", key=f"update_{habit[0]}"):
                    update_habit(habit[0], new_name, new_target)
                    st.rerun()

                if st.button("Delete", key=f"delete_{habit[0]}"):
                    delete_habit(habit[0])
                    st.rerun()

    # ---------- TRACK ---------- #

    if menu == "Track":

        habits = get_user_habits(st.session_state.user_id)

        with st.form("track_form"):

            for habit in habits:

                habit_name = habit[2].lower()

                if "study" in habit_name:
                    st.number_input(
                        f"{habit[2]} (Enter Study Hours)",
                        min_value=0,
                        max_value=24,
                        key=f"value_{habit[0]}"
                    )
                else:
                    st.checkbox(
                        f"{habit[2]}",
                        key=f"value_{habit[0]}"
                    )

            submit = st.form_submit_button("Submit")

            if submit:
                for habit in habits:
                    habit_name = habit[2].lower()

                    if "study" in habit_name:
                        val = st.session_state[f"value_{habit[0]}"]
                        if val > 0:
                            log_habit(habit[0], val)
                    else:
                        checked = st.session_state[f"value_{habit[0]}"]
                        if checked:
                            log_habit(habit[0], 1)

                st.success("Logged Successfully")
                st.rerun()

    # ---------- DASHBOARD ---------- #

    if menu == "Dashboard":
        show_dashboard(st.session_state.user_id)

    # ---------- PDF ---------- #

    if menu == "PDF":
        file_path = generate_pdf_report(st.session_state.user_id)
        with open(file_path, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name="Habit_Report.pdf",
                mime="application/pdf"
            )
