import streamlit as st
import pandas as pd
from database import get_connection
from style import apply_style

apply_style()

st.title("📊 Community Dashboard")

# Load data from database instead of session_state
conn = get_connection()
df = pd.read_sql_query("SELECT * FROM moods", conn)
conn.close()

if df.empty:
    st.info("No emotional data available yet.")
else:
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Assessments", len(df))
    col2.metric("Areas Covered", df["area"].nunique())
    col3.metric("Most Common Mood", df["mood"].mode()[0])

    st.markdown("---")

    st.bar_chart(df["mood"].value_counts())
