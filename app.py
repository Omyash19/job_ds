import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import random

# 1. PAGE CONFIG
st.set_page_config(
    page_title="ECHOES | Global Tech Intelligence", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. MAPPING & CONSTANTS
COUNTRY_MAP = {
    "at": "Austria", "au": "Australia", "be": "Belgium", "br": "Brazil", 
    "ca": "Canada", "ch": "Switzerland", "de": "Germany", "es": "Spain", 
    "fr": "France", "gb": "United Kingdom", "in": "India", "it": "Italy", 
    "mx": "Mexico", "nl": "Netherlands", "nz": "New Zealand", "pl": "Poland", 
    "sg": "Singapore", "us": "United States", "za": "South Africa"
}
COUNTRY_FLAGS = {
    "au": "🇦🇺", "br": "🇧🇷", "ca": "🇨🇦", "fr": "🇫🇷", "de": "🇩🇪", "in": "🇮🇳", 
    "ie": "🇮🇪", "nl": "🇳🇱", "pl": "🇵🇱", "sg": "🇸🇬", "us": "🇺🇸", "gb": "🇬🇧"
}
TECH_ROLES = ["Data Engineer", "Data Scientist", "Data Analyst", "Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Machine Learning Engineer", "DevOps Engineer"]

# 3. ADVANCED UI FINISHING (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"], [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #0f172a; }
    .stApp { background: #F8FAFC; }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }

    .hero-title { text-align: center; color: #0f172a; font-weight: 800; font-size: 3.5rem; margin-top: 40px; }
    .hero-subtitle { text-align: center; color: #6366f1; font-size: 1.1rem; margin-bottom: 30px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; }
    .section-header { text-align: center; color: #0f172a; font-weight: 800; font-size: 2.2rem; margin-bottom: 20px; }

    /* Glassmorphism Configuration Card - Full Width Single Column */
    [data-testid="column"] > div[data-testid="stVerticalBlock"]:has(.config-card-marker) {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid white;
        border-radius: 32px;
        padding: 50px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05);
        max-width: 800px;
        margin: 0 auto;
    }

    /* Glassmorphism Inputs */
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"], div[data-testid="stRadio"] > div {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(20px);
        border: 1px solid white !important;
        border-radius: 12px !important;
    }

    /* Primary buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 14px;
        font-weight: 700;
        height: 3.5em;
        font-size: 1rem;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button { border-radius: 12px; font-weight: 600; }

    /* Insight Guide Footer */
    .insight-footer {
        background: rgba(99, 102, 241, 0.05);
        padding: 20px;
        border-radius: 16px;
        border-left: 4px solid #6366f1;
        margin-top: 30px;
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .job-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        padding: 25px 35px;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 1px solid white;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 4. DATA ENGINE (Dummy Data for UI)
@st.cache_data
def load_data():
    companies = ["Google", "Meta", "Stripe", "Airbnb", "Netflix"]
    data = []
    for _ in range(20):
        data.append({
            "title": random.choice(TECH_ROLES),
            "company": random.choice(companies),
            "country": "us",
            "location": "Remote",
            "salary_min": 100000,
            "salary_max": 150000,
            "url": "#",
            "country_code": "us"
        })
    df = pd.DataFrame(data)
    df['country_name'] = df['country_code'].map(COUNTRY_MAP).fillna("United States")
    return df

raw_df = load_data()

# 5. STATE MANAGEMENT
if 'page' not in st.session_state: st.session_state.page = "landing"
if 'filters' not in st.session_state: st.session_state.filters = {}

# 6. APP CONTENT
if not raw_df.empty:
    
    # LANDING PAGE
    if st.session_state.page == "landing":
        st.markdown('<h1 class="hero-title">ECHOES 💎</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">The Intelligence Layer for Global Tech</p>', unsafe_allow_html=True)
        _, center, _ = st.columns([1, 2, 1])
        with center:
            if st.button("Launch Job Explorer", use_container_width=True, type="primary"):
                st.session_state.page = "config_explorer"; st.rerun()
            if st.button("Access Intelligence", use_container_width=True):
                st.session_state.page = "config_analytics"; st.rerun()

    # CONFIGURATION PAGE (Redesigned Flow)
    elif st.session_state.page in ["config_explorer", "config_analytics"]:
        st.markdown('<h2 class="section-header">Configure Your Insight</h2>', unsafe_allow_html=True)
        
        _, center_col, _ = st.columns([1, 4, 1])
        
        with center_col:
            # Marker for CSS Styling
            st.markdown("<div class='config-card-marker'></div>", unsafe_allow_html=True)
            
            # STEP 1: FILTERS (Top)
            st.markdown("<h4 style='margin-top:0; color:#0f172a;'>1. Set Data Parameters</h4>", unsafe_allow_html=True)
            sel_regions = st.multiselect("Target Regions", sorted(raw_df['country_name'].unique().tolist()), default=[raw_df['country_name'].unique().tolist()[0]])
            
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                sel_currency = st.radio("Financial Currency", ["USD", "INR"], horizontal=True)
            with f_col2:
                sel_role = "All Roles"
                if st.session_state.page == "config_explorer":
                    sel_role = st.selectbox("Tech Stack Preference", ["All Roles"] + TECH_ROLES)
            
            st.markdown("<div style='height: 20px; border-bottom: 1px solid rgba(0,0,0,0.05); margin-bottom:30px;'></div>", unsafe_allow_html=True)

            # STEP 2: ACTION (Middle)
            btn_label = "Search Live Market" if st.session_state.page == "config_explorer" else "Generate Market Report"
            if st.button(btn_label, use_container_width=True, type="primary"):
                st.session_state.filters = {"regions": sel_regions, "currency": sel_currency, "role": sel_role, "rate": 83.5 if sel_currency == "INR" else 1.0}
                st.session_state.page = "results_explorer" if st.session_state.page == "config_explorer" else "results_analytics"
                st.rerun()
            
            # STEP 3: INSIGHT GUIDE (Bottom)
            st.markdown(f"""
                <div class="insight-footer">
                    <strong>💡 Insight Guide:</strong><br/>
                    Select multiple regions to compare macro-economic tech trends. 
                    { "Setting a specific tech stack preference allows ECHOES to filter the noise and deliver high-precision benchmarks." if st.session_state.page == "config_explorer" else "Reports include real-time salary variance and demand distribution." }
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            if st.button("← Back to Home", use_container_width=True):
                st.session_state.page = "landing"; st.rerun()

    # Placeholders for Result Views
    elif "results" in st.session_state.page:
        st.button("← Back to Configuration", on_click=lambda: setattr(st.session_state, 'page', 'config_explorer' if 'explorer' in st.session_state.page else 'config_analytics'))
        st.write("Results will appear here based on dummy data.")
