import streamlit as st
from datetime import datetime
from database import get_connection, create_tables
from style import apply_style
import pandas as pd

apply_style()
create_tables()

st.title("👥 My Local Circle")

st.markdown("""
<div style='text-align:center; margin-bottom:20px;'>
    <h3 style='color:#00f2ff;'>Banjara Hills Support Group</h3>
    <p>Members: 6 / 8 | Next Meet-up: Sunday 5 PM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# Post Message
# -----------------------------
st.subheader("💬 Share with Your Circle")

message = st.text_area("Write something supportive...")

if st.button("Post"):
    if message.strip() == "":
        st.error("Please write something before posting.")
    else:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO circle_posts (message, time)
            VALUES (?, ?)
        """, (
            message,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))

        conn.commit()
        conn.close()

        st.success("Message shared with your circle 💛")
        st.rerun()

st.markdown("---")

# -----------------------------
# Display Posts
# -----------------------------
st.subheader("🧡 Circle Wall")

conn = get_connection()
posts_df = pd.read_sql_query(
    "SELECT * FROM circle_posts ORDER BY id DESC",
    conn
)
conn.close()

if posts_df.empty:
    st.info("No posts yet. Be the first to share something 🌟")
else:
    for _, row in posts_df.iterrows():
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.05);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(0,242,255,0.2);
        ">
            <p style="font-size:16px;">{row['message']}</p>
            <p style="font-size:12px; color:gray;">🕒 {row['time']}</p>
        </div>
        """, unsafe_allow_html=True)
