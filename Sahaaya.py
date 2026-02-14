import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta
from database import get_connection, create_tables

create_tables()

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Sahaaya Circles Dashboard",
    page_icon="💛",
    layout="wide"
)

# ---------------------------------------------------
# Custom Futuristic Styling
# ---------------------------------------------------
st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-left: 5rem;
    padding-right: 5rem;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    color: white;
}

[data-testid="stSidebarNav"] > div:first-child {
    display: none;
}

[data-testid="stSidebarNav"] a {
    font-size: 16px;
    padding: 10px 12px;
    border-radius: 10px;
    margin-bottom: 6px;
    color: white;
}

[data-testid="stSidebarNav"] a:hover {
    background-color: #1f2937;
    box-shadow: 0px 0px 8px #00f2ff;
}

.stMetric {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0,242,255,0.2);
}

h1, h2, h3 {
    text-align: center;
    color: #00f2ff;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Sidebar Branding
# ---------------------------------------------------
st.sidebar.markdown("""
<div style='text-align:center; padding:20px;'>
    <h2 style='color:#00f2ff;'>💛 SAHAAYA</h2>
    <p style='color:gray;'>Emotional Intelligence System</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# ---------------------------------------------------
# Demo Mode Toggle
# ---------------------------------------------------
demo_mode = st.sidebar.toggle("🎭 Enable Demo Mode")

st.sidebar.markdown("---")  
st.sidebar.subheader("⚙ Data Controls")

# Clear real database data
if st.sidebar.button("🗑 Clear All Real Data"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM moods")
    conn.commit()
    conn.close()
    st.sidebar.success("All real data has been cleared.")
    st.rerun()

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
if demo_mode:

    demo_data = []

    sample_areas = ["Gachibowli", "Jubilee Hills", "Banjara Hills"]
    sample_moods = ["Happy 😊", "Neutral 😐", "Stressed 😔", "Lonely 😢"]

    for _ in range(25):
        demo_data.append({
            "Age": random.randint(16, 65),
            "Mood": random.choice(sample_moods),
            "Problems": ["Work Stress"],
            "Severity": random.randint(3, 9),
            "Area": random.choice(sample_areas),
            "Time": datetime.now() - timedelta(days=random.randint(0, 5))
        })

    df = pd.DataFrame(demo_data)

else:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM moods", conn)
    conn.close()

    if not df.empty:
        df.rename(columns={
            "age": "Age",
            "mood": "Mood",
            "problems": "Problems",
            "severity": "Severity",
            "area": "Area",
            "time": "Time"
        }, inplace=True)

# ---------------------------------------------------
# Animated Overview Section
# ---------------------------------------------------
st.markdown("""
<style>
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade {
    animation: fadeInUp 1.2s ease-out;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="fade" style="text-align:center; padding:60px 20px;">
    <h1 style="color:#00f2ff; font-size:48px;">💛 SAHAAYA</h1>
    <h3>For the emotional well-being of our communities</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="fade" style="background:rgba(255,255,255,0.05);
    padding:25px;border-radius:15px;text-align:center;
    backdrop-filter:blur(10px);
    box-shadow:0 0 20px rgba(0,242,255,0.2);">
    <h4 style="color:#00f2ff;">🌍 Why Sahaaya?</h4>
    <p>Urban loneliness is increasing. Communities lack structured emotional support systems.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="fade" style="background:rgba(255,255,255,0.05);
    padding:25px;border-radius:15px;text-align:center;
    backdrop-filter:blur(10px);
    box-shadow:0 0 20px rgba(0,242,255,0.2);">
    <h4 style="color:#00f2ff;">🧠 What It Does</h4>
    <p>Calculates Emotional Risk Index and activates local volunteer support.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="fade" style="background:rgba(255,255,255,0.05);
    padding:25px;border-radius:15px;text-align:center;
    backdrop-filter:blur(10px);
    box-shadow:0 0 20px rgba(0,242,255,0.2);">
    <h4 style="color:#00f2ff;">📊 What It Presents You</h4>
    <p>Geo analytics, risk alerts, dashboards, and community events.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# Dashboard Section
# ---------------------------------------------------
if df.empty:
    st.markdown("""
    <div style="text-align:center; padding:40px;">
        <p>Submit a mood check-in or enable Demo Mode.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    col1, col2, col3 = st.columns(3)

    col1.metric("🧾 Total Assessments", len(df))
    col2.metric("📍 Areas Covered", df["Area"].nunique())
    col3.metric("😊 Most Common Mood", df["Mood"].mode()[0])

    st.markdown("---")

    score_map = {
        "Happy 😊": 2,
        "Neutral 😐": 1,
        "Stressed 😔": -1,
        "Lonely 😢": -2
    }

    df["Score"] = df["Mood"].map(score_map)
    community_score = round(df["Score"].mean(), 2)

    st.subheader("💛 Community Emotional Index")
    st.metric("Current Index", community_score)

    if community_score < 0:
        st.error("🚨 Community stress levels rising")
    else:
        st.success("🟢 Community emotional health stable")

    st.markdown("---")

    st.subheader("📈 Emotional Severity Trend")

    df["Date"] = pd.to_datetime(df["Time"]).dt.date
    trend = df.groupby("Date")["Severity"].mean()

    st.line_chart(trend)
