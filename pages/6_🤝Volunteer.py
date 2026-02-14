import streamlit as st
from database import get_connection, create_tables
from style import apply_style

apply_style()
create_tables()

st.title("🤝 Register as a Community Helper")

with st.form("helper_form"):

    name = st.text_input("Your Name")
    area = st.text_input("Your Area")

    age_group = st.multiselect(
        "Age Group You Want to Support",
        ["Children", "Teenagers", "Adults", "Elderly"]
    )

    skills = st.multiselect(
        "How can you help?",
        ["Listening", "Student Mentoring", "Stress Support", "Career Guidance"]
    )

    volunteering_type = st.selectbox(
        "Volunteering Type",
        ["One-Time", "Weekly", "Emergency"]
    )

    mode = st.selectbox("Mode", ["Online", "Offline", "Both"])
    availability = st.selectbox("Availability", ["Weekends", "Evenings", "Flexible"])

    submit = st.form_submit_button("Register")

    if submit:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO volunteers
            (name, area, age_group, skills, volunteering_type, mode, availability)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            area,
            ",".join(age_group),
            ",".join(skills),
            volunteering_type,
            mode,
            availability
        ))

        conn.commit()
        conn.close()

        st.success("You are now a Sahaaya Helper 💛")
