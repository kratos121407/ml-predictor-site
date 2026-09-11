import streamlit as st
from style import inject_css, hero

st.set_page_config(
    page_title="ML Prediction Hub",
    page_icon="🔮",
    layout="centered",
)

inject_css()

hero(
    "🔮 ML Prediction Hub",
    "Three machine learning tools, one place. Pick a predictor from the sidebar to get started.",
)

st.markdown("### Available Predictors")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """<div class="card">
        <h4>🍷 Wine Quality</h4>
        <p>Enter chemical properties (acidity, sugar, alcohol, etc.) to predict Good vs Bad wine quality.</p>
        </div>""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """<div class="card">
        <h4>💼 Hiring Decision</h4>
        <p>Enter a candidate's skills, education, and certifications to predict Hire vs Reject.</p>
        </div>""",
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """<div class="card">
        <h4>🕵️ Job Posting Check</h4>
        <p>Paste a job posting's details to predict whether it's Real or Fake.</p>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(
    "👈 **Use the sidebar** to open each predictor, enter your values, "
    "and get an instant prediction."
)
