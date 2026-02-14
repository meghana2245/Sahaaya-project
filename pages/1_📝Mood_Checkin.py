import streamlit as st
from datetime import datetime
from database import get_connection, create_tables
from style import apply_style

apply_style()
create_tables()

st.title("📝 Mood Check-in")

with st.form("mood_form", clear_on_submit=True):

    age = st.number_input("👤 Age", min_value=10, max_value=100)

    mood = st.selectbox(
        "💭 How are you feeling today?",
        ["", "Happy 😊", "Neutral 😐", "Stressed 😔", "Lonely 😢"]
    )

    problem_type = st.multiselect(
        "📌 What challenges are you facing?",
        [
            "Academic Pressure",
            "Work Stress",
            "Family Issues",
            "Financial Concerns",
            "Health Issues",
            "Relationship Problems",
            "Loneliness",
            "Career Uncertainty",
        ]
    )

    severity = st.slider(
        "📊 Emotional Intensity Level (1 = Mild, 10 = Severe)",
        1, 10
    )

    positive_note = st.text_area("✨ Additional thoughts (optional)")
    area = st.text_input("📍 Enter Your Area")

    submit = st.form_submit_button("Submit")

    if submit:

        if mood == "" or area.strip() == "":
            st.error("⚠ Please fill all required fields.")
        
        elif mood != "Happy 😊" and len(problem_type) == 0:
            st.error("⚠ Please select at least one challenge.")
        
        else:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO moods 
                (age, mood, problems, severity, note, area, time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                age,
                mood,
                ",".join(problem_type),
                severity,
                positive_note,
                area,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))

            conn.commit()
            conn.close()

            st.success("💛 Mood submitted successfully.")
