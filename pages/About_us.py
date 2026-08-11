import streamlit as st
from PIL import Image
import os

# ==========================================
# 1. BASE SYSTEM & GLOBAL CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Curiosity Hub",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. ADVANCED FRONTEND INTERFACE OPTIMIZATION (CSS)
# ==========================================

# UTILITY 1: UI Override to force-hide Streamlit's native multipage links
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# UTILITY 2: Brand Styling Integration (Google Fonts & Typography Grid)
st.markdown("""
    <style>
    /* Import Studio Typography Package from Google Core Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    /* Apply Poppins Bold to all application titles and headers */
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# UTILITY 3: Layout Alignment & Custom Canvas Adjustments
st.markdown("""
    <style>
    /* Minimizes default header padding to maximize visual space at the top */
    [data-testid="stSidebarNav"] {
        padding-top: 1rem !important;
    }
    
    /* Premium graphic asset framework for Yashwi's Studio Logo */
    .sidebar-logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 8px;
        background-color: #1A1A2E;
        padding: 6px;
        border: 1px solid #2A2A4A;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 3. SIDEBAR BRANDING & EXECUTIVE ENGINE
# ==========================================
with st.sidebar:
    # Build a horizontal micro-grid columns layout to pair Logo next to App Name
    logo_col, text_col = st.columns([1, 2])
    
    with logo_col:
        # Renders the transparent workspace logo asset
        st.image("logo.png", use_container_width=True)
        
    with text_col:
        # Dynamically scales the corporate title next to the brand image
        st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 30px;'>Curiosity Hub</h1>", unsafe_allow_html=True)
    st.markdown("### 🧭 Navigation")
    
    # Homepage Button
    if st.button("🏠 Homepage", use_container_width=True):
        st.switch_page("Homepage.py")
        
    # Science Page Button
    if st.button("🔬 Science", use_container_width=True):
        st.switch_page("pages/Science.py")
        
    # SST Page Button
    if st.button("📚 SST", use_container_width=True):
        st.switch_page("pages/Sst.py")
    if st.button("❓ Quiz", use_container_width=True):
        st.switch_page("pages/Quiz.py")
    # About Us Page Button
    if st.button("ℹ️ About Us", use_container_width=True):
        st.switch_page("pages/About_us.py")
    # Structural border line separating brand identity from upcoming custom navigation
    st.write("---") 
    # General brand greeting section in the sidebar
   

# ==========================================
# 4. MAIN CENTRAL PANEL APPLICATION DISPLAY
# ==========================================

# Core Welcome Matrix Header
st.markdown("<h1 style='text-align: center;'>📖Welcome to Curiosity Hub!📗📘📙</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color:#C4C7CE'>This is an app specifically designed to help 8th grade students with their studies by providing them good quality notes and tests.</h3>", unsafe_allow_html=True)

# Strategic Core Objective Layer (Our Aim Section)
st.markdown("<h2 style='color:#00A896;'>Our Aim🎯</h2>", unsafe_allow_html=True)
st.markdown("<h3 >To provide high-quality educational resources that enhance learning and improve academic performance for 8th grade students. Another aim behind this app is to make learning more engaging, accessible and uniform, so we can grow together.</h3>", unsafe_allow_html=True)

# Quality Assurance Layer (Securing System Credibility)
st.markdown("<h2 style='color:#FF9F43;'>Quality Ensured 🛡️</h2>", unsafe_allow_html=True)
st.markdown("<h3 >Every resource you see on this app is carefully designed and checked for accuracy and relevance before being made available to users.</h3>", unsafe_allow_html=True)

# Operational Personnel Directory (The Core Workspace Leads)
st.markdown("<h2 style='color:#6C5CE7;'>Lead Contributors 📝</h2>", unsafe_allow_html=True)
st.markdown("<h3>1. Keshav Gupta (Tech & Engineering Lead)</h3>", unsafe_allow_html=True)
st.markdown("<h3>2. Devanshi Panwar (Core Content & Research Lead)</h3>", unsafe_allow_html=True)
st.markdown("<h3>3. Yashvi Bhardwaj (UI & Creative Design Lead)</h3>", unsafe_allow_html=True)