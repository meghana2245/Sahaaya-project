import streamlit as st
import pandas as pd
from database import get_connection
from style import apply_style

apply_style()

st.title("🤝 Find Nearby Support")

conn = get_connection()
helpers_df = pd.read_sql_query("SELECT * FROM volunteers", conn)
conn.close()

age_input = st.number_input("👤 Your Age", min_value=10, max_value=100)

# Determine age group
if age_input <= 12:
    user_group = "Children"
elif age_input <= 19:
    user_group = "Teenagers"
elif age_input <= 59:
    user_group = "Adults"
else:
    user_group = "Elderly"



problem_input = st.selectbox(
    "📌 What problem are you facing?",
    [
        "",
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

area_input = st.text_input("📍 Enter Your Area")

search = st.button("🔍 Find Support")

if search:

    if helpers_df.empty:
        st.warning("No volunteers registered yet.")
    
    else:
        filtered = helpers_df[
            helpers_df["area"].str.lower() == area_input.lower()
        ]

        if filtered.empty:
            st.warning("No volunteers found in this area.")
        else:
            st.success(f"Found {len(filtered)} volunteers 💛")

            for _, row in filtered.iterrows():
                st.markdown(f"""
                ### 🤝 {row['name']}
                📍 Area: {row['area']}
                🛠 Skills: {row['skills']}
                ⏰ Availability: {row['availability']}
                """)
                st.markdown("---")
