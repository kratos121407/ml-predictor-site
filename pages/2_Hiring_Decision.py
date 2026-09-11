import streamlit as st
import joblib
import os
import numpy as np
from style import inject_css, hero

st.set_page_config(page_title="Hiring Decision", page_icon="💼", layout="centered")
inject_css()
hero("💼 AI Hiring Decision", "Enter a candidate's profile to predict Hire vs Reject.")

MODEL_PATH = os.path.join("models", "hiring_model.pkl")


@st.cache_resource
def load_bundle():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


bundle = load_bundle()

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### Candidate Profile")

experience = st.number_input("Experience (Years)", min_value=0, max_value=40, value=3, step=1)
projects = st.number_input("Projects Count", min_value=0, max_value=50, value=3, step=1)
salary = st.number_input("Salary Expectation ($)", min_value=0, max_value=500000, value=70000, step=1000)

job_roles = bundle["job_roles"] if bundle else ["AI Researcher", "Data Scientist", "Software Engineer", "Cybersecurity Analyst"]
job_role = st.selectbox("Job Role", job_roles)

education_levels = bundle["education_levels"] if bundle else ["B.Sc", "B.Tech", "M.Tech", "MBA", "PhD"]
education = st.selectbox("Education", education_levels)

certifications = bundle["certifications"] if bundle else ["None", "Google ML", "Deep Learning Specialization", "AWS Certified"]
certification = st.selectbox("Certification", certifications)

skill_columns = bundle["skill_columns"] if bundle else [
    "C++", "Cybersecurity", "Deep Learning", "Ethical Hacking", "Java", "Linux",
    "Machine Learning", "NLP", "Networking", "Python", "Pytorch", "React", "SQL", "TensorFlow",
]
selected_skills = st.multiselect("Skills", skill_columns)

st.markdown("</div>", unsafe_allow_html=True)

if st.button("Predict Hiring Decision", key="predict_hiring"):
    if bundle is None:
        st.warning(
            "No trained model found yet. Upload hiring_model.pkl to the models/ "
            "folder to get real predictions."
        )
    else:
        education_map_bachelor = {"B.Sc": 1, "B.Tech": 1, "M.Tech": 1, "MBA": 1, "PhD": 1}
        education_map_master = {"B.Sc": 0, "B.Tech": 0, "M.Tech": 1, "MBA": 1, "PhD": 1}
        education_map_phd = {"B.Sc": 0, "B.Tech": 0, "M.Tech": 0, "MBA": 0, "PhD": 1}

        if job_role in ["AI Researcher", "Data Scientist"]:
            cert_fit = 1 if certification in ["Google ML", "Deep Learning Specialization"] else 0
        elif job_role in ["Cybersecurity Analyst", "Software Engineer"]:
            cert_fit = 1 if certification == "AWS Certified" else 0
        else:
            cert_fit = 0

        if salary <= 50000:
            salary_bracket = 0
        elif salary <= 80000:
            salary_bracket = 1
        elif salary <= 100000:
            salary_bracket = 2
        else:
            salary_bracket = 3

        row = {
            "Experience (Years)": experience,
            "Projects Count": projects,
            "Bachelor_or_above": education_map_bachelor[education],
            "Master_or_above": education_map_master[education],
            "PhD": education_map_phd[education],
            "Certification_Fit": cert_fit,
            "Salary_Bracket": salary_bracket,
        }
        for skill in skill_columns:
            row[skill] = 1 if skill in selected_skills else 0

        x = np.array([[row[feat] for feat in bundle["feature_order"]]])
        pred = bundle["model"].predict(x)[0]

        label = "✅ Hire" if pred == 1 else "❌ Reject"
        st.markdown(f'<div class="result-box">{label}</div>', unsafe_allow_html=True)
