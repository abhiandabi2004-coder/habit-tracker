import streamlit as st
from database import create_tables
from habit_engine import (
    add_habit,
    get_user_habits,
    update_habit,
    delete_habit,
    log_habit,
)
from dashboard import show_dashboard
from pdf_export import generate_pdf_report

create_tables()

st.title("🔥 Habit Tracker")

if "user_id" not in st.session_state:
    st.session_state.user_id = 1  # Demo user

menu = st.sidebar.radio(
    "Menu", ["Add/Edit Habits", "Track", "Dashboard", "PDF"]
)

# ---------------- ADD / EDIT ---------------- #

if menu == "Add/Edit Habits":

    st.subheader("Add New Habit")

    habit_name = st.text_input("Habit Name")
    target_days = st.number_input("Target Days", 1, 365)

    if st.button("Add Habit"):
        add_habit(st.session_state.user_id, habit_name, target_days)
        st.success("Habit Added")
        st.rerun()

    st.subheader("Edit Existing Habits")

    habits = get_user_habits(st.session_state.user_id)

    for habit in habits:
        with st.expander(f"{habit[2]}"):
            new_name = st.text_input(
                "New Name", value=habit[2], key=f"name_{habit[0]}"
            )
            new_target = st.number_input(
                "New Target", value=habit[3], key=f"target_{habit[0]}"
            )

            if st.button("Update", key=f"update_{habit[0]}"):
                update_habit(habit[0], new_name, new_target)
                st.success("Updated")
                st.rerun()

            if st.button("Delete", key=f"delete_{habit[0]}"):
                delete_habit(habit[0])
                st.success("Deleted")
                st.rerun()

# ---------------- TRACK ---------------- #

elif menu == "Track":

    habits = get_user_habits(st.session_state.user_id)

    with st.form("track_form"):
        for habit in habits:
            st.number_input(
                f"{habit[2]} (Enter Hours/Value)",
                min_value=0,
                max_value=24,
                key=f"value_{habit[0]}",
            )

        submit = st.form_submit_button("Submit")

        if submit:
            for habit in habits:
                val = st.session_state[f"value_{habit[0]}"]
                if val > 0:
                    log_habit(habit[0], val)

            st.success("Logged Successfully")
            st.rerun()

# ---------------- DASHBOARD ---------------- #

elif menu == "Dashboard":
    show_dashboard(st.session_state.user_id)

# ---------------- PDF ---------------- #

elif menu == "PDF":
    file_path = generate_pdf_report(st.session_state.user_id)
    with open(file_path, "rb") as f:
        st.download_button("Download PDF", f)
