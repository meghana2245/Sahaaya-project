import streamlit as st

def apply_style():

    st.markdown("""
    <style>

    /* Main background */
    .main {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }

    /* Equal spacing */
    .block-container {
        padding-top: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111827;
        color: white;
    }

    /* Hide default app label */
    [data-testid="stSidebarNav"] > div:first-child {
        display: none;
    }

    /* Sidebar links */
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

    /* Metric Cards */
    .stMetric {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(0,242,255,0.2);
    }

    /* Center titles */
    h1, h2, h3 {
        text-align: center;
        color: #00f2ff;
    }

    </style>
    """, unsafe_allow_html=True)
