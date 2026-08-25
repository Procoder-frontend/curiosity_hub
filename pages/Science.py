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

# ==========================================
# 4. SORT FUNCTION
# ==========================================
def natural_sort_key(text):
    return [
        int(c) if c.isdigit() else c.lower()
        for c in re.split(r'(\d+)', text)
    ]

# ==========================================
# 5. HEADER
# ==========================================
st.title("🔬 Science")

st.markdown("""
Explore the natural world through **Physics, Chemistry,
and Biology.**
""")

st.info(
    "📘 Curiosity Hub notes are designed for quick revision and conceptual understanding. But reading NCRET beforehand is highly recommended."
)

st.write("")

# ==========================================
# 6. SUBJECT CARDS
# Check whether someone is logged in
if "user_id" not in st.session_state:
    st.error("Please log in first.")
    st.stop()

response = (
    supbase
    .table("users")
    .select("profile")
    .eq("id", st.session_state["user_id"])
    .execute()
)

if not response.data:
    st.error("User profile not found.")
    st.stop()

profile = response.data[0]["profile"]
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='subject-box'>
    <h2>⚛ Physics</h2>
    <p>Motion, force, energy and the laws of nature.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='subject-box'>
    <h2>🧪 Chemistry</h2>
    <p>Matter, mixtures, reactions and materials.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='subject-box'>
    <h2>🌿 Biology</h2>
    <p>Life, cells, plants and living organisms.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==========================================
# 7. TABS
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "⚛ Physics",
    "🧪 Chemistry",
    "🌿 Biology"
])

subjects = {
    "Physics": tab1,
    "Chemistry": tab2,
    "Biology": tab3
}

# ==========================================
# 8. PDF ENGINE
# ==========================================
for subject, tab in subjects.items():

    folder = os.path.join("science", subject.lower())

    with tab:

        st.subheader(subject)

        if os.path.exists(folder):

            pdf_files = [
                f for f in os.listdir(folder)
                if f.endswith(".pdf")
            ]

            pdf_files.sort(key=natural_sort_key)

            if pdf_files:

                for filename in pdf_files:

                    clean_name = (
                        filename
                        .replace(".pdf", "")
                        .replace("_", " ")
                    )

                    path = os.path.join(folder, filename)

                    with open(path, "rb") as pdf:
                        data = pdf.read()

                    st.markdown(
                        f"""
                        <div class='note-card'>
                        <h3>📄 {clean_name}</h3>
                        <p>Compressed revision notes for quick learning.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.download_button(
                        label="📥 Download Notes",
                        data=data,
                        file_name=filename,
                        mime="application/pdf",
                        key=f"{subject}_{filename}",
                        use_container_width=True
                    ):

                        note_name = filename.replace(".pdf", "")

                        if note_name not in profile["science_notes"]:

                            profile["science_notes"].append(note_name)

                            response = (
                                supbase
                                .table("users")
                                .update({"profile": profile})
                                .eq("id", st.session_state["user_id"])
                                .execute()
                            )
                        st.success("Progress updated!")

                        st.write("")

        else:
            st.warning( 
                f"{subject} folder not found."
            )