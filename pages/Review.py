import streamlit as st
import os
import re
import json
from supabase import create_client
SUPABASE_URL = "https://kmukvcojgcxegsadqotp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImttdWt2Y29qZ2N4ZWdzYWRxb3RwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODYxMTA3NjUsImV4cCI6MjEwMTY4Njc2NX0._0H5j6hr8c07XZk_xKUGB_qMDVu0LlrE4MNJJeHdomc"

supbase = create_client(SUPABASE_URL, SUPABASE_KEY)
# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Curiosity Hub",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)
# ==========================================
# 2. CSS
# ==========================================
st.markdown("""
<style>

[data-testid="stSidebarNav"] {
    display: none !important;
}

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

h1,h2,h3,h4,h5,h6 {
    font-family: 'Poppins', sans-serif !important;
}

.block-container {
    padding-top: 1rem;
}

.stTabs [data-baseweb="tab"] p {
    font-size: 20px !important;
    font-weight: 600 !important;
}

.note-card {
    background-color: #161B22;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #30363D;
    margin-bottom: 15px;
}

.subject-box {
    background-color: #151924;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR
# ==========================================
with st.sidebar:

    logo_col, text_col = st.columns([1,2])

    with logo_col:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            pass

    with text_col:
        st.markdown(
            "<h1 style='font-size:30px;'>Curiosity Hub</h1>",
            unsafe_allow_html=True
        )

    st.markdown("### 🧭 Navigation")

    if st.button("🏠 Homepage", use_container_width=True):
        st.switch_page("Homepage.py")

    if st.button("🔬 Science", use_container_width=True):
        st.switch_page("pages/Science.py")

    if st.button("📚 SST", use_container_width=True):
        st.switch_page("pages/Sst.py")

    if st.button("❓ Quiz", use_container_width=True):
        st.switch_page("pages/Quiz.py")

    if st.button("ℹ️ About Us", use_container_width=True):
        st.switch_page("pages/About_us.py")

    if st.button("📝 Review", use_container_width=True):
            st.switch_page("pages/Review.py")
        
    st.write("---")
