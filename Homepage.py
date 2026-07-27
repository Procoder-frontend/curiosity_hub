import streamlit as st
import os
import re
import json
import random
def count_files(root_folder, extension):
    total = 0

    for root, dirs, files in os.walk(root_folder):
        total += len([
            f for f in files
            if f.endswith(extension)
        ])

    return total
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

/* HERO TITLE */

.hero-title {
    text-align: center;
    font-size: 75px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 10px;
}

/* HERO SUBTITLE */

.hero-subtitle {
    text-align: center;
    font-size: 40px;
    font-weight: 600;
    margin-bottom: 30px;
    line-height: 1.5;
}

/* QUOTE */

.quote-text {
    text-align: center;
    font-size: 24px;
    font-style: italic;
    color: #D1D5DB;
    margin-top: 20px;
}

/* TABLETS */

@media (max-width: 768px) {

    .hero-title {
        font-size: 55px;
    }

    .hero-subtitle {
        font-size: 28px;
    }

    .quote-text {
        font-size: 20px;
    }

}

/* PHONES */

@media (max-width: 480px) {

    .hero-title {
        font-size: 42px;
    }

    .hero-subtitle {
        font-size: 24px;
    }

    .quote-text {
        font-size: 18px;
    }

}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR BRANDING & EXECUTIVE ENGINE
# ==========================================
def create_user_profile(name):

    # Create users folder automatically if missing
    if not os.path.exists("users"):
        os.mkdir("users")

    # Generate unique ID
    user_id = f"{name}_{random.randint(1000,9999)}"

    # Prevent duplicate IDs
    while os.path.exists(f"users/{user_id}.json"):
        user_id = f"{name}_{random.randint(1000,9999)}"

    # User profile structure
    profile = {
        "name": name,
        "id": user_id,
        "science_notes": [],
        "sst_notes": [],
        "sst_quizzes": [],
        "science_quizzes": [],
    }

    # Save profile
    with open(f"users/{user_id}.json", "w") as file:
        json.dump(profile, file, indent=4)

    # Remember who logged in
    st.session_state["user_id"] = user_id

    return profile

TOTAL_SCIENCE_NOTES = count_files("science", ".pdf")
TOTAL_SST_NOTES = count_files("sst", ".pdf")

TOTAL_SCIENCE_QUIZZES = count_files("sci_quizes", ".json")
TOTAL_SST_QUIZZES = count_files("sst_quizes", ".json")
with st.sidebar:
    # Build a horizontal micro-grid columns layout to pair Logo next to App Name
    logo_col, text_col = st.columns([1, 2])

    with logo_col:
        st.image("logo.png", use_container_width=True)

    with text_col:
        st.markdown(
            "<h1 style='text-align: center; font-weight: 700; font-size: 30px;'>Curiosity Hub</h1>",
            unsafe_allow_html=True
        )

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
        st.switch_page("pages/About_Us.py")

    st.write("---")

    # ==========================
    # ACCOUNT SECTION
    # ==========================

        # ==========================
    # ACCOUNT SECTION
    # ==========================

# ==========================
# ACCOUNT SECTION
# ==========================

    st.subheader("👤 Account")

    # Default session variables
    if "login_mode" not in st.session_state:
        st.session_state["login_mode"] = False

    if "show_new_id" not in st.session_state:
        st.session_state["show_new_id"] = None

    name = st.text_input(
        "Enter your name",
        placeholder="e.g. Keshav"
    )

    # -------------------------
    # STEP 1 : CREATE / LOGIN
    # -------------------------

    if st.button("Create / Login", use_container_width=True):

        if name.strip() == "":
            st.warning("Please enter your name.")

        else:

            if not os.path.exists("users"):
                os.mkdir("users")

            matches = []

            for file in os.listdir("users"):

                if file.endswith(".json"):

                    with open(os.path.join("users", file), "r") as f:
                        data = json.load(f)

                    if data["name"].lower() == name.lower():
                        matches.append(data)

            # New user
            if len(matches) == 0:

                profile = create_user_profile(name)

                st.session_state["show_new_id"] = profile["id"]

                st.rerun()

            # Existing name
            else:

                st.session_state["pending_name"] = name
                st.session_state["choose_action"] = True
                st.rerun()

    # -------------------------
    # STEP 2 : SHOW NEW USER ID
    # -------------------------

    if st.session_state["show_new_id"]:

        st.success("🎉 Account created successfully!")

        st.info(f"""
## Your User ID

### {st.session_state["show_new_id"]}

⚠️ Save this ID carefully.
You will need it whenever you log in.
""")

        if st.button("Continue", use_container_width=True):

            st.session_state["show_new_id"] = None
            st.rerun()

    # -------------------------
    # STEP 3 : NAME EXISTS
    # -------------------------

    if st.session_state.get("choose_action", False):

        st.warning("This name already exists.")

        col1, col2 = st.columns(2)

        with col1:

            if st.button("🔑 Login", use_container_width=True):

                st.session_state["login_mode"] = True
                st.session_state["choose_action"] = False
                st.rerun()

        with col2:

            if st.button("➕ Create New Account", use_container_width=True):

                profile = create_user_profile(st.session_state["pending_name"])

                st.session_state["show_new_id"] = profile["id"]

                st.session_state["choose_action"] = False

                st.rerun()

    # -------------------------
    # STEP 4 : LOGIN
    # -------------------------

    if st.session_state.get("login_mode", False):

        entered_id = st.text_input("Enter your User ID")

        if st.button("Login", use_container_width=True):

            path = f"users/{entered_id}.json"

            if os.path.exists(path):

                with open(path, "r") as f:
                    profile = json.load(f)

                if profile["name"].lower() == st.session_state["pending_name"].lower():

                    st.session_state["user_id"] = profile["id"]

                    del st.session_state["pending_name"]

                    st.session_state["login_mode"] = False

                    st.success(f"Welcome {profile['name']}!")

                    st.rerun()

                else:

                    st.error("User ID does not match this name.")

            else:

                st.error("Invalid User ID.")

    st.write("---")
#Main Page Content

    
with open("quotes.json", "r") as file:
    quotes = json.load(file)
st.markdown("""
<div class="hero-title">
    Curiosity <span style="color:#864df7;">Hub</span>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="hero-subtitle">
    ✨<span style="color:#6faff7;">Study</span>
    →
    <span style="color:#4bd439;">Learn</span>
    →
    <span style="color:#c4b510;">Test</span>
    →
    <span style="color:#e33636;">Repeat</span>✨
</div>
""", unsafe_allow_html=True)
quote = random.choice(quotes)
st.write("")
st.markdown(f"<h4 style='text-align: center;font-weight: 400;'>\"{quote}\"</h4>", unsafe_allow_html=True)
######
# Check if someone is logged in
if "user_id" not in st.session_state:
    st.error("No user logged in.")
    st.stop()

USER_PATH = f'users/{st.session_state["user_id"]}.json'

with open(USER_PATH, "r") as file:
    profile = json.load(file)
science_progress = int(
    len(profile["science_notes"])
    / TOTAL_SCIENCE_NOTES
    * 100
)

sst_progress = int(
    len(profile["sst_notes"])
    / TOTAL_SST_NOTES
    * 100
)

quiz_progress = int(
    (
        len(profile["science_quizzes"])
        +
        len(profile["sst_quizzes"])
    )
    /
    (TOTAL_SCIENCE_QUIZZES + TOTAL_SST_QUIZZES)
    * 100
)
######

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='subject-box'>
    <h2>👨‍🔬SCIENCE</h2>
    <p>Compressed notes, important concepts and chapter quizzes.</p>
    </div>
    """, unsafe_allow_html=True)

    #science_progress = 55
    st.progress(science_progress/100)
    st.write(f"📈 {science_progress}% Complete")

with col2:
    st.markdown("""
    <div class='subject-box'>
    <h2>🌍 SST</h2>
    <p>History, Geography and Civics notes with revision material.</p>
    </div>
    """, unsafe_allow_html=True)

    #sst_progress = 45

    #
    st.progress(sst_progress/100)
    st.write(f"📈 {sst_progress}% Complete")

with col3:
    st.markdown("""
    <div class='subject-box'>
    <h2>❓ QUIZ</h2>
    <p>Practice questions and track your learning progress.</p>
    </div>
    """, unsafe_allow_html=True)
    #quiz_progress = 30
    st.progress(quiz_progress/100)
    st.write(f"📈 {quiz_progress}% Complete")