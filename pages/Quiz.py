import streamlit as st
import json
import os
import random
import re

# ==========================================
# 1. BASE CONFIGURATION
# ==========================================

def natural_sort_key(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

st.set_page_config(
    page_title="Curiosity Hub",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. GLOBAL CSS SYSTEM
# ==========================================

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none !important;
}

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.block-container {
    padding-top: 1rem;
}

h1, h2, h3, h4, h5 {
    font-weight: 700 !important;
}

.stTabs [data-baseweb="tab"] p {
    font-size: 20px !important;
    font-weight: 600 !important;
}

.hero-card {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    padding: 35px;
    border-radius: 20px;
    margin-bottom: 25px;
}

.hero-title {
    color: white;
    font-size: 42px;
    font-weight: 700;
}

.hero-subtitle {
    color: #CBD5E1;
    font-size: 18px;
}

.quiz-card {
    background-color: #1E2533;
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #2C3445;
    margin-bottom: 20px;
}

.subject-card {
    background-color: #1E2533;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #2C3445;
    margin-bottom: 20px;
}

.question-badge {
    background: #2563EB;
    color: white;
    padding: 8px 20px;
    border-radius: 20px;
    display: inline-block;
    font-weight: bold;
    margin-bottom: 15px;
}

.result-card {
    background: linear-gradient(135deg, #1E3C72 0%, #2A5298 100%);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
}

.answer-correct {
    background: #1F4D2B;
    border: 2px solid #4CAF50;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.answer-wrong {
    background: #4A231F;
    border: 2px solid #E74C3C;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.answer-right {
    background: #203B2C;
    border: 1px dashed #4CAF50;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR SYSTEM
# ==========================================

with st.sidebar:
    logo_col, text_col = st.columns([1, 2])
    
    with logo_col:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.warning("Logo missing")

    with text_col:
        st.markdown("<h1 style='font-size:28px; text-align:center;'>Curiosity Hub</h1>", unsafe_allow_html=True)

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

    st.write("---")
    st.caption("Curiosity Hub Quiz Engine")

# ==========================================
# 4. HERO SECTION
# ==========================================

st.markdown("""
<div class="hero-card">
    <div class="hero-title">🧠 Curiosity Hub Quiz Arena</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. QUIZ STATISTICS
# ==========================================

sst_count = 0
sci_count = 0

if os.path.exists("sst_quizes"):
    sst_count = len([f for f in os.listdir("sst_quizes") if f.endswith(".json")])

if os.path.exists("sci_quizes"):
    sci_count = len([f for f in os.listdir("sci_quizes") if f.endswith(".json")])

col1, col2, col3 = st.columns(3)
col1.metric("📚 SST Chapters", sst_count)
col2.metric("🧪 Science Chapters", sci_count)
col3.metric("🧠 Total Quizzes", sst_count + sci_count)
st.write("")

# ==========================================
# 6. SESSION STATE
if "user_id" not in st.session_state:
    st.error("Please log in first.")
    st.stop()

USER_PATH = f'users/{st.session_state["user_id"]}.json'

with open(USER_PATH, "r") as file:
    profile = json.load(file)

if "active_quiz_id" not in st.session_state:
    st.session_state.active_quiz_id = None

# ==========================================
# 7. QUIZ ENGINE START
# ==========================================

def run_quiz_engine(quiz_title, json_filename):
    if st.button("⬅ Exit Quiz", use_container_width=True):
        st.session_state.active_quiz_id = None
        for key in ["active_quiz_set", "current_q", "score", "user_responses", "quiz_finished"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    st.markdown(f"## 📘 {quiz_title}")
    st.write("---")

    pool = []
    try:
        with open(json_filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                found_key = None
                for key in data.keys():
                    if "pool" in key.lower():
                        found_key = key
                        break
                if found_key:
                    pool = data[found_key]
                else:
                    pool = next(iter(data.values())) if data else []
            elif isinstance(data, list):
                pool = data
    except FileNotFoundError:
        st.error(f"{json_filename} not found.")
        return
    except json.JSONDecodeError:
        st.error(f"{json_filename} is corrupted.")
        return

    if "active_quiz_set" not in st.session_state:
        valid_pool = [
            q for q in pool 
            if isinstance(q, dict) and q.get("question") and len(q.get("options", [])) >= 2
        ]

        if len(valid_pool) == 0:
            st.error("No valid questions found.")
            return

        sample_size = min(len(valid_pool), 15)
        st.session_state.active_quiz_set = random.sample(valid_pool, sample_size)
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.user_responses = {}
        st.session_state.quiz_finished = False

    quiz_set = st.session_state.active_quiz_set
    total_q = len(quiz_set)

    # ==========================================
    # RESULT SCREEN
    # ==========================================
    if st.session_state.quiz_finished:
        final_score = st.session_state.score
        accuracy = int((final_score / total_q) * 100)

        if accuracy == 100:
            title = "🏆 Quiz Master"
        elif accuracy >= 90:
            title = "⭐ Expert"
        elif accuracy >= 75:
            title = "📘 Scholar"
        elif accuracy >= 60:
            title = "📚 Learner"
        else:
            title = "🔁 Explorer"

        st.markdown(f"""
        <div class="result-card">
            <h1>🏁 Quiz Complete!</h1>
            <h2>{title}</h2>
            <p>Review your performance below.</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        c1.metric("🎯 Score", f"{final_score}/{total_q}")
        c2.metric("📈 Accuracy", f"{accuracy}%")
        st.write("")

        if accuracy == 100:
            st.balloons()
            st.success("Perfect performance. Outstanding work.")
        elif accuracy >= 80:
            st.success("Excellent understanding of the chapter.")
        elif accuracy >= 60:
            st.info("Good effort. A little revision can improve your score.")
        else:
            st.warning("Review the chapter and try again.")

        if st.button("🔄 Return to Quiz Dashboard", use_container_width=True):
            st.session_state.active_quiz_id = None
            for key in ["active_quiz_set", "current_q", "score", "user_responses", "quiz_finished"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        return

    # ==========================================
    # ACTIVE QUESTION
    # ==========================================
    idx = st.session_state.current_q
    current_question = quiz_set[idx]

    metric1, metric2 = st.columns([3, 1])
    with metric1:
        st.markdown(f"### 📊 Progress: {idx+1}/{total_q}")
        st.progress((idx + 1) / total_q)
    with metric2:
        running = int((st.session_state.score / idx) * 100) if idx > 0 else 0
        st.metric("Accuracy", f"{running}%")

    st.write("")
    st.markdown(f'<div class="question-badge">Question {idx+1}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="quiz-card"><h3>{current_question["question"]}</h3></div>', unsafe_allow_html=True)

    saved_answer = st.session_state.user_responses.get(idx)
    answered = saved_answer is not None
    correct_char = current_question.get("answer", "")

    for option in current_question["options"]:
        correct = option.startswith(correct_char)

        if saved_answer == option:
            if correct:
                st.markdown(f'<div class="answer-correct">🟢 {option}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="answer-wrong">❌ {option}</div>', unsafe_allow_html=True)
        else:
            if answered and correct:
                st.markdown(f'<div class="answer-right">✔ {option}</div>', unsafe_allow_html=True)
            else:
                if st.button(option, key=f"q_{idx}_{option}", use_container_width=True, disabled=answered):
                    st.session_state.user_responses[idx] = option
                    if correct:
                        st.session_state.score += 1
                    st.rerun()

    st.write("")
    nav1, space, nav2 = st.columns([1, 2, 1])

    with nav1:
        if st.button("← Previous", disabled=(idx == 0), use_container_width=True):
            st.session_state.current_q -= 1
            st.rerun()

    with nav2:
        if idx < total_q - 1:
            if st.button("Next →", use_container_width=True):
                st.session_state.current_q += 1
                st.rerun()
        else:
            if st.button("🏁 Finish Quiz", use_container_width=True):
                final_score = st.session_state.score
                accuracy = int((final_score / total_q) * 100)

                # Corrected logic boundaries inside the action block:
                if accuracy >= 80:
                    quiz_name = os.path.basename(json_filename).replace(".json", "")
                    if "Science" in quiz_title:
                        if quiz_name not in profile["science_quizzes"]:
                            profile["science_quizzes"].append(quiz_name)
                    else:
                        if quiz_name not in profile["sst_quizzes"]:
                            profile["sst_quizzes"].append(quiz_name)

                    with open(USER_PATH, "w") as file:
                        json.dump(profile, file, indent=4)

                st.session_state.quiz_finished = True
                st.rerun()

# ==========================================
# DASHBOARD
# ==========================================
if st.session_state.active_quiz_id is None:
    tab1, tab2 = st.tabs(["📚 SST", "🧪 Science"])

    # ======================
    # SST TAB
    # ======================
    with tab1:
        st.markdown("### Social Science Quizzes")
        sst_folder = "sst_quizes"

        if os.path.exists(sst_folder):
            files = sorted(os.listdir(sst_folder))
            json_files = [f for f in files if f.endswith(".json")]

            for filename in json_files:
                clean_name = filename.replace("_", " ").replace(".json", "").title()
                path = os.path.join(sst_folder, filename)

                with st.container(border=True):
                    st.subheader(f"📘 {clean_name}")
                    st.caption("15 random questions.")
                    if st.button(f"🚀 Start {clean_name}", key=f"sst_{filename}", use_container_width=True):
                        st.session_state.active_quiz_id = (f"SST - {clean_name}", path)
                        st.rerun()

    # ======================
    # SCIENCE TAB
    # ======================
    with tab2:
        st.markdown("### Science Quizzes")
        sci_folder = "sci_quizes"

        if os.path.exists(sci_folder):
            files = os.listdir(sci_folder)
            json_files = [f for f in files if f.endswith(".json")]
            json_files.sort(key=natural_sort_key)

            for filename in json_files:
                clean_name = filename.replace("_", " ").replace(".json", "").title()
                path = os.path.join(sci_folder, filename)

                with st.container(border=True):
                    st.subheader(f"🧪 {clean_name}")
                    st.caption("15 random questions.")
                    if st.button(f"🚀 Start {clean_name}", key=f"sci_{filename}", use_container_width=True):
                        st.session_state.active_quiz_id = (f"Science - {clean_name}", path)
                        st.rerun()
else:
    quiz_title, json_path = st.session_state.active_quiz_id
    run_quiz_engine(quiz_title, json_path)