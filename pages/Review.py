import streamlit as st
import os
import re
import datetime
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
.review-card {
    background-color: #161B22;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #30363D;
    margin-bottom: 15px;
}

.review-header {
    font-size: 20px;
    font-weight: 600;
}

.review-text {
    font-size: 17px;
    margin-top: 10px;
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
#st.title("⭐ Review Curiosity Hub")

# st.markdown(
#     """
#     ### Your feedback matters

#     Tell us how Curiosity Hub is working for you.

#     Your **rating is required**, but writing a review is completely optional.
#     Even a single rating helps us understand how we are doing.
#     """
# )

# st.divider()

# ==========================================
# 4. LOGIN REQUIREMENT
# ==========================================

# Check whether the user is logged in
if "user_id" not in st.session_state:

    st.title("⭐ Review Curiosity Hub")

    st.warning("🔒 Please log in or create an account to submit a review.")

    st.info(
        "You need a Curiosity Hub account because your review is linked "
        "to your account."
    )

    if st.button("🏠 Go to Homepage", use_container_width=True):
        st.switch_page("Homepage.py")

    st.stop()


# ==========================================
# 5. GET LOGGED-IN USER PROFILE
# ==========================================

response = (
    supbase
    .table("users")
    .select("profile")
    .eq("id", st.session_state["user_id"])
    .execute()
)

# Check whether the stored account still exists
if not response.data:

    st.warning(
        "⚠️ Your session is no longer valid. Please log in again."
    )

    st.session_state.pop("user_id", None)

    if st.button("🏠 Return to Homepage", use_container_width=True):
        st.switch_page("Homepage.py")

    st.stop()


# Get profile
profile = response.data[0]["profile"]

user_id = profile["id"]
user_name = profile["name"]


# ==========================================
# 6. REVIEW PAGE
# ==========================================

st.title("⭐ Review Curiosity Hub")

st.markdown(
    f"""
    ### Your feedback matters

    Welcome, **{user_name}**.

    Tell us how Curiosity Hub is working for you.

    Your **rating is required**, but writing a review is completely optional.
    Even a single rating helps us understand how we are doing.
    """
)

st.divider()


# ==========================================
# 7. REVIEW FORM
# ==========================================

st.subheader("⭐ How would you rate Curiosity Hub?")

rating = st.radio(
    "Rating",
    options=[1, 2, 3, 4, 5],
    format_func=lambda x: "⭐" * x,
    horizontal=True,
    index=None,
)

st.subheader("📝 Want to tell us more?")

review_text = st.text_area(
    "Your review (optional)",
    placeholder=(
        "Tell us what you liked, what could be improved, "
        "or what you would like to see next..."
    ),
    height=150,
    max_chars=1000,
)

st.caption(
    "You can submit with only a rating if you don't want to write anything."
)


# ==========================================
# 8. SUBMIT REVIEW
# ==========================================

if st.button("🚀 Submit Review", use_container_width=True):

    # Rating is mandatory
    if rating is None:

        st.error("⭐ Please select a rating before submitting.")

    else:

        try:

            cleaned_review = review_text.strip()

            supbase.table("reviews").insert({
                "user_id": user_id,
                "name": user_name,
                "rating": rating,
                "review": cleaned_review if cleaned_review else None,
                "approved": False
            }).execute()

            st.success(
                "🎉 Thank you! Your feedback has been submitted."
            )

            st.info(
                "Your review may appear publicly after it has been reviewed."
            )

        except Exception as e:

            st.error(
                "Something went wrong while submitting your review."
            )

            st.write(e)
# ==========================================
# 9. DISPLAY APPROVED REVIEWS
# ==========================================

st.divider()

st.header("💬 What students are saying")

try:

    reviews_response = (
        supbase
        .table("reviews")
        .select("name, rating, review, created_at")
        .eq("approved", True)
        .order("created_at", desc=True)
        .execute()
    )

    reviews = reviews_response.data

    if not reviews:

        st.info(
            "No approved reviews yet. Be one of the first to share your experience!"
        )

    else:

        for review in reviews:

            name = review.get("name", "Student")
            rating_value = review.get("rating", 0)
            written_review = review.get("review")
            st.divider()
            st.markdown(f"### {name}")

            st.write("⭐" * rating_value)

            if written_review:
                st.write(f'"{written_review}"')
            else:
                st.caption("No written review.")

            st.divider()

except Exception as e:

    st.error("Reviews could not be loaded.")

    st.write(e)

