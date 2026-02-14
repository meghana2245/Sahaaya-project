import streamlit as st
from style import apply_style
from database import get_connection, create_tables
from datetime import datetime, date
import pandas as pd

apply_style()
create_tables()

st.title("📅 Community Events Hub 🌍")

conn = get_connection()
cursor = conn.cursor()

# -----------------------------
# Default Events (Insert Only If Table Empty)
# -----------------------------
cursor.execute("SELECT COUNT(*) FROM events")
count = cursor.fetchone()[0]

if count == 0:
    default_events = [
        ("Sunday Park Support Circle",
         "Jubilee Hills Park",
         "2026-03-15",
         "Open community discussion on stress and work-life balance.",
         datetime.now().strftime("%Y-%m-%d %H:%M")),
        ("Student Mentorship Meetup",
         "Gachibowli Library",
         "2026-03-18",
         "Guidance and emotional support session for college students.",
         datetime.now().strftime("%Y-%m-%d %H:%M")),
        ("Senior Citizens Tea Gathering",
         "Banjara Hills Community Hall",
         "2026-03-20",
         "Friendly conversation circle for elderly community members.",
         datetime.now().strftime("%Y-%m-%d %H:%M"))
    ]

    cursor.executemany("""
        INSERT INTO events (title, location, event_date, description, created)
        VALUES (?, ?, ?, ?, ?)
    """, default_events)

    conn.commit()

st.markdown("---")

# -----------------------------
# Add New Event Section
# -----------------------------
st.subheader("➕ Create New Community Event")

with st.form("event_form"):
    event_name = st.text_input("Event Title")
    location = st.text_input("Location")
    event_date = st.date_input("Event Date")
    description = st.text_area("Short Description")

    submitted = st.form_submit_button("Add Event")

    if submitted:
        if event_name and location:
            cursor.execute("""
                INSERT INTO events (title, location, event_date, description, created)
                VALUES (?, ?, ?, ?, ?)
            """, (
                event_name,
                location,
                event_date.strftime("%Y-%m-%d"),
                description,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))

            conn.commit()
            st.success("🎉 Event Added Successfully!")
        else:
            st.warning("Please fill required fields.")

st.markdown("---")

# -----------------------------
# Display Events
# -----------------------------
st.subheader("📌 Upcoming Community Events")

events_df = pd.read_sql_query("SELECT * FROM events ORDER BY event_date ASC", conn)

st.metric("Total Active Events", len(events_df))

for _, event in events_df.iterrows():
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 0 0 15px rgba(0,242,255,0.2);
    ">
        <h4 style="color:#00f2ff;">{event['title']}</h4>
        <p><strong>📍 Location:</strong> {event['location']}</p>
        <p><strong>📅 Date:</strong> {event['event_date']}</p>
        <p>{event['description']}</p>
    </div>
    """, unsafe_allow_html=True)

conn.close()
