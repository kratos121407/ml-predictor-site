import streamlit as st
import joblib
import os
import numpy as np
from style import inject_css, hero

st.set_page_config(page_title="Wine Quality", page_icon="🍷", layout="centered")
inject_css()
hero("🍷 Wine Quality Checker", "Enter the wine's chemical properties to predict if it's Good or Bad quality.")

MODEL_PATH = os.path.join("models", "wine_quality.pkl")

FEATURES = [
    ("fixed acidity", 7.4, 4.0, 16.0),
    ("volatile acidity", 0.70, 0.1, 1.6),
    ("citric acid", 0.00, 0.0, 1.0),
    ("residual sugar", 1.9, 0.5, 16.0),
    ("chlorides", 0.076, 0.01, 0.6),
    ("free sulfur dioxide", 11.0, 1.0, 72.0),
    ("total sulfur dioxide", 34.0, 6.0, 290.0),
    ("density", 0.9978, 0.99, 1.004),
    ("pH", 3.51, 2.7, 4.0),
    ("sulphates", 0.56, 0.3, 2.0),
    ("alcohol", 9.4, 8.0, 15.0),
]


@st.cache_resource
def load_bundle(path):
    if os.path.exists(path):
        return joblib.load(path)
    return None


bundle = load_bundle(MODEL_PATH)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### Wine Properties")

values = {}
cols = st.columns(2)
for i, (name, default, lo, hi) in enumerate(FEATURES):
    with cols[i % 2]:
        values[name] = st.number_input(
            name.replace("_", " ").title(),
            value=float(default),
            min_value=float(lo) * 0.3,
            max_value=float(hi) * 1.5,
            step=0.01,
            format="%.4f",
        )

st.markdown("</div>", unsafe_allow_html=True)

if st.button("Predict Wine Quality", key="predict_wine"):
    x = np.array([[values[name] for name, _, _, _ in FEATURES]])

    if bundle is not None:
        model = bundle["model"]
        scaler = bundle.get("scaler")
        x_input = scaler.transform(x) if scaler is not None else x
        pred = model.predict(x_input)[0]
        label = "🍷 Good Quality" if pred == 1 else "⚠️ Bad Quality"
        st.markdown(f'<div class="result-box">{label}</div>', unsafe_allow_html=True)
    else:
        st.warning(
            "No trained model found yet. Upload wine_quality.pkl to the models/ "
            "folder (see README) to get real predictions."
        )
