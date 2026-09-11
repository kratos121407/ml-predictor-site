import streamlit as st
import joblib
import os
import numpy as np
from scipy.sparse import hstack, csr_matrix
from style import inject_css, hero

st.set_page_config(page_title="Job Posting Check", page_icon="🕵️", layout="centered")
inject_css()
hero("🕵️ Real or Fake Job Posting?", "Paste in a job posting's details to check if it looks fraudulent.")

MODEL_PATH = os.path.join("models", "job_postings_model.pkl")


@st.cache_resource
def load_bundle(path):
    if os.path.exists(path):
        return joblib.load(path)
    return None


bundle = load_bundle(MODEL_PATH)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### Job Text")

title = st.text_input("Job Title", "Marketing Intern")
company_profile = st.text_area("Company Profile", "", height=80)
description = st.text_area("Job Description", "", height=120)
requirements = st.text_area("Requirements", "", height=100)
benefits = st.text_area("Benefits", "", height=80)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### Job Details")

OTHER = "Other / Unknown"


def options_for(col, fallback):
    if bundle:
        return [OTHER] + bundle["categorical_options"].get(col, fallback)
    return [OTHER] + fallback


location = st.selectbox("Location", options_for("location", []))
department = st.selectbox("Department", options_for("department", []))
employment_type = st.selectbox(
    "Employment Type", options_for("employment_type", ["Full-time", "Part-time", "Contract", "Temporary", "Other"])
)
required_experience = st.selectbox(
    "Required Experience",
    options_for("required_experience", ["Internship", "Entry level", "Mid-Senior level", "Director", "Executive"]),
)
required_education = st.selectbox(
    "Required Education", options_for("required_education", ["High School", "Bachelor's Degree", "Master's Degree"])
)
industry = st.selectbox("Industry", options_for("industry", []))
function = st.selectbox("Function", options_for("function", []))

col1, col2, col3 = st.columns(3)
with col1:
    telecommuting = st.checkbox("Telecommuting")
with col2:
    has_company_logo = st.checkbox("Has Company Logo")
with col3:
    has_questions = st.checkbox("Has Screening Questions")

st.markdown("</div>", unsafe_allow_html=True)

if st.button("Check Posting", key="predict_jobs"):
    if bundle is None:
        st.warning(
            "No trained model found yet. Upload job_postings_model.pkl to the "
            "models/ folder to get real predictions."
        )
    else:
        combined_text = " ".join([title, company_profile, description, requirements, benefits])
        X_text = bundle["tfidf"].transform([combined_text])

        numeric_values = {
            "telecommuting": int(telecommuting),
            "has_company_logo": int(has_company_logo),
            "has_questions": int(has_questions),
        }
        X_numeric = csr_matrix(np.array([[numeric_values[c] for c in bundle["numeric_columns"]]], dtype=float))

        selections = {
            "location": location,
            "department": department,
            "employment_type": employment_type,
            "required_experience": required_experience,
            "required_education": required_education,
            "industry": industry,
            "function": function,
        }
        encoded_row = np.zeros((1, len(bundle["encoded_columns"])))
        for i, col_name in enumerate(bundle["encoded_columns"]):
            for cat_col, value in selections.items():
                if value != OTHER and col_name == f"{cat_col}_{value}":
                    encoded_row[0, i] = 1
        X_encoded = csr_matrix(encoded_row)

        X_final = hstack([X_text, X_numeric, X_encoded]).tocsr()
        pred = bundle["model"].predict(X_final)[0]

        label = "🚩 Likely FAKE" if pred == 1 else "✅ Likely Real"
        st.markdown(f'<div class="result-box">{label}</div>', unsafe_allow_html=True)
