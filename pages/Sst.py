import streamlit as st
from PIL import Image
import os
import json
from supabase import create_client
SUPABASE_URL = "https://kmukvcojgcxegsadqotp.supabase.co"
SUPABASE_KEY ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImttdWt2Y29qZ2N4ZWdzYWRxb3RwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODYxMTA3NjUsImV4cCI6MjEwMTY4Njc2NX0._0H5j6hr8c07XZk_xKUGB_qMDVu0LlrE4MNJJeHdomc"

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

h1, h2, h3, h4, h5, h6 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

.stTabs [data-baseweb="tab"] p {
    font-size: 20px !important;
    font-weight: 600 !important;
}

.subject-card {
    background-color: #151924;
    border: 1px solid #303040;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    margin-bottom: 20px;
}

.note-card {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
}

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
# 3. SIDEBAR
# ==========================================
with st.sidebar:

    logo_col, text_col = st.columns([1, 2])

    with logo_col:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            pass

    with text_col:
        st.markdown(
            "<h1 style='text-align:center; font-size:30px;'>Curiosity Hub</h1>",
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
        st.switch_page("pages/About_Us.py")
    
    if st.button("📝 Review", use_container_width=True):
        st.switch_page("pages/Review.py")
        
    st.write("---")

# ==========================================
# 4. MAIN HEADER
# ==========================================
st.title("🌍 Social Studies")

st.markdown("""
Explore **History, Geography and Civics**
through compressed notes designed for
quick revision and conceptual understanding.
""")

st.info(
    "📘 Curiosity Hub SST notes preserve important NCERT concepts while reducing unnecessary information. But reading NCRET beforehand is highly recommended."
)

st.write("")

# ==========================================
# 5. SUBJECT CARDS
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="subject-card">
        <h2>📜 History</h2>
        <p>Civilizations, events, empires and important historical developments.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="subject-card">
        <h2>🌱 Geography</h2>
        <p>Earth, environment, resources and the relationship between humans and nature.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="subject-card">
        <h2>⚖️ Civics</h2>
        <p>Government, citizenship, rights, duties and social responsibility.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==========================================
# 6. TABS
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
tab1, tab2, tab3 = st.tabs([
    "📜 History",
    "🌱 Geography",
    "⚖️ Civics"
])

base_dir = "sst"


# ==========================================
# 7. HISTORY
# ==========================================
with tab1:

    st.header("📜 History")

    st.markdown("""
    Study civilizations, kingdoms, revolutions,
    and the events that shaped human society.
    """)

    history_folder = os.path.join(base_dir, "history")

    if os.path.exists(history_folder):

        files = sorted(os.listdir(history_folder))

        pdf_files = [
            f for f in files
            if f.endswith(".pdf")
        ]

        if pdf_files:

            for filename in pdf_files:

                clean_name = (
                    filename
                    .replace("_", " ")
                    .replace(".pdf", "")
                    .replace("hard", "(Available for difficult chapters)")
                )

                full_path = os.path.join(
                    history_folder,
                    filename
                )

                with open(full_path, "rb") as pdf_file:
                    binary_data = pdf_file.read()

                with st.container(border=True):

                    st.markdown(
                        f"### 📄 {clean_name}"
                    )

                    st.caption(
                        "Compressed revision notes for quick learning."
                    )

                    if st.download_button(
                        label="📥 Download Notes",
                        data=binary_data,
                        file_name=filename,
                        mime="application/pdf",
                        key=f"history_{filename}",
                        use_container_width=True
                    ):

                        note_name = filename.replace(".pdf", "")

                        if note_name not in profile["sst_notes"]:

                            profile["sst_notes"].append(note_name)

                            supbase.table("users").update(
                            {"profile": profile}
                            ).eq(
                            "id", st.session_state["user_id"]
                            ).execute()

                            st.success("Progress updated!")
                    st.write("")

        else:
            st.info("No History notes available.")

# ==========================================
# 8. GEOGRAPHY
# ==========================================
with tab2:

    st.header("🌱 Geography")

    st.markdown("""
    Explore the world's diverse landscapes, climates, and natural features.
    """)

    geography_folder = os.path.join(base_dir, "geography")

    if os.path.exists(geography_folder):

        files = sorted(os.listdir(geography_folder))

        pdf_files = [
            f for f in files
            if f.endswith(".pdf")
        ]

        if pdf_files:

            for filename in pdf_files:

                clean_name = (
                    filename
                    .replace("_", " ")
                    .replace(".pdf", "")
                )

                full_path = os.path.join(
                    geography_folder,
                    filename
                )

                with open(full_path, "rb") as pdf_file:
                    binary_data = pdf_file.read()

                with st.container(border=True):

                    st.markdown(
                        f"### 📄 {clean_name}"
                    )

                    st.caption(
                        "Compressed revision notes for quick learning."
                    )

                    if st.download_button(
                        label="📥 Download Notes",
                        data=binary_data,
                        file_name=filename,
                        mime="application/pdf",
                        key=f"geography_{filename}",
                        use_container_width=True
                    ):

                        note_name = filename.replace(".pdf", "")

                        if note_name not in profile["sst_notes"]:

                            profile["sst_notes"].append(note_name)

                            supbase.table("users").update(
                                {"profile": profile}
                                ).eq(
                                "id", st.session_state["user_id"]
                            ).execute()

                            st.success("Progress updated!")

                    st.write("")

        else:
            st.info("No Geography notes available.")


# ==========================================
# 9. CIVICS
# ==========================================
with tab3:

    st.header("⚖️ Civics")

    st.markdown("""
    Learn about government, democracy,
    rights, duties and citizenship.
    """)

    civics_folder = os.path.join(base_dir, "civics")

    if os.path.exists(civics_folder):

        files = sorted(os.listdir(civics_folder))

        pdf_files = [
            f for f in files
            if f.endswith(".pdf")
        ]

        if pdf_files:

            for filename in pdf_files:

                clean_name = (
                    filename
                    .replace("_", " ")
                    .replace(".pdf", "")
                )

                if "hard" in filename.lower():
                    clean_name = clean_name.replace(
                        "hard",
                        "(Available for difficult chapters)"
                    )

                full_path = os.path.join(
                    civics_folder,
                    filename
                )

                with open(full_path, "rb") as pdf_file:
                    binary_data = pdf_file.read()

                with st.container(border=True):

                    st.markdown(
                        f"### 📄 {clean_name}"
                    )

                    st.caption(
                        "Compressed revision notes for quick learning."
                    )

                    if st.download_button(
                        label="📥 Download Notes",
                        data= binary_data,
                        file_name=filename,
                        mime="application/pdf",
                        key=f"civics_{filename}",
                        use_container_width=True
                    ):

                        note_name = filename.replace(".pdf", "")

                        if note_name not in profile["sst_notes"]:

                            profile["sst_notes"].append(note_name)

                            supbase.table("users").update(
                                {"profile": profile}
                                ).eq(
                                "id", st.session_state["user_id"]
                            ).execute()

                            st.success("Progress updated!")

                    st.write("")

        else:
            st.info("No Civics notes available.")