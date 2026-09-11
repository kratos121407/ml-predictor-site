import streamlit as st

CUSTOM_CSS = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .hero {
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #6C63FF 0%, #8F87FF 100%);
        color: white;
        margin-bottom: 1.5rem;
    }
    .hero h1 {
        color: white;
        margin-bottom: 0.3rem;
    }
    .hero p {
        color: #EDEBFF;
        font-size: 1.05rem;
        margin: 0;
    }

    .card {
        background: #F4F5FA;
        border-radius: 14px;
        padding: 1.5rem;
        border: 1px solid #E4E4F0;
        margin-bottom: 1rem;
    }

    .result-box {
        background: #EDF9F0;
        border: 1px solid #B8E6C1;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
        color: #1A7A3C;
    }

    .stButton>button {
        background-color: #6C63FF;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        border: none;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #574FE0;
        color: white;
    }
</style>
"""

def inject_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def hero(title: str, subtitle: str):
    st.markdown(
        f"""<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>""",
        unsafe_allow_html=True,
    )
