import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# 1. PAGE CONFIG (Force Sidebar Collapsed)
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
TECH_ROLES = ["Data Engineer", "Data Scientist", "Data Analyst", "Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Machine Learning Engineer", "DevOps Engineer"]
SKILL_KEYWORDS = ["Python", "SQL", "AWS", "Azure", "Docker", "Kubernetes", "Spark", "React", "Tableau", "Snowflake", "Java"]

# 3. VERBATIM LAYOUT CSS (Recreating image_22.png visual balance)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: white; }
    
    /* Dark Theme Background (verbatim from image) */
    .main { background: #0c0e12; }
    
    /* Center Title and Buttons (verbatim from image) */
    .center-branding { text-align: center; color: white; margin-top: 60px; margin-bottom: 20px; }
    
    /* KPI Metric Cards (verbatim from image) */
    div[data-testid="stMetric"] {
        background: rgba(99, 102, 241, 0.04) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(99, 102, 241, 0.1);
        padding: 25px;
        border-radius: 20px;
    }
    div[data-testid="stMetricValue"] { color: #6366f1 !important; font-weight: 800 !important; font-size: 2.2rem !important; }
    div[data-testid="stMetricLabel"] { color: #64748b !important; font-weight: 700 !important; text-transform: uppercase; font-size: 0.8rem; }

    /* Horizontal Glass Job Card (Verbatim Structure from image_22.png) */
    .job-card-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #31333f;
        padding: 20px 30px;
        border-radius: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .job-card-container:hover {
        background: #3c3e4a;
        transform: translateY(-3px);
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    /* Fine Print info (Left side verbatim) */
    .fine-print-info {
        flex: 1;
        min-width: 0;
    }
    .job-title { margin:0; color:white; font-weight:800; font-size:1.6rem; display: flex; align-items: center; gap: 10px;}
    .company-info { color: #818cf8; font-weight: 700; margin: 8px 0; font-size: 1rem;}
    .salary-info { color: #64748b; font-size: 0.9rem; font-weight: 400; margin-top: 12px;}

    /* Apply Button (Right side verbatim, matching blue background in ref) */
    .apply-now-btn {
        background-color: #6366f1;
        color: white !important;
        padding: 12px 28px;
        border-radius: 14px;
        text-decoration: none;
        font-weight: 700;
        font-size: 14px;
        white-space: nowrap;
        margin-left: 20px;
        transition: opacity 0.2s;
    }
    .apply-now-btn:hover { opacity: 0.9; }

    /* Expandable Description Box */
    .desc-box { color: #475569; font-size: 1rem; line-height: 1.7; padding: 25px; background: white; border-radius: 20px; margin-bottom: 40px; border: 1px solid #f1f5f9; }
    </style>
""", unsafe_allow_html=True)

# 4. DATA ENGINE
@st.cache_data(ttl=3600)
def load_data():
    db_url = st.secrets["DATABASE_URL"]
    engine = create_engine(db_url)
    df = pd.read_sql("SELECT * FROM tech_jobs", engine)
    df['salary_min'] = pd.to_numeric(df['salary_min'], errors='coerce').fillna(0)
    df['salary_max'] = pd.to_numeric(df['salary_max'], errors='coerce').fillna(0)
    df['country_code'] = df['country'].str.lower()
    df['country_name'] = df['country_code'].map(COUNTRY_MAP).fillna(df['country_code'].str.upper())
    return df

try:
    raw_df = load_data()
except:
    raw_df = pd.DataFrame()

# 5. STATE MANAGEMENT
if 'page' not in st.session_state: st.session_state.page = "landing"
if 'filters' not in st.session_state: st.session_state.filters = {}

def set_page(page_name):
    st.session_state.page = page_name

# 6. APP CONTENT BY STAGE
if not raw_df.empty:
    
    # ─── VIEW 1: LANDING PAGE ───
    if st.session_state.page == "landing":
        st.markdown('<div class="center-branding"><h1>ECHOES 💎</h1></div>', unsafe_allow_html=True)
        nav_l, n1, n2, nav_r = st.columns([1, 2, 2, 1])
        with n1:
            if st.button("🔍 Open Job Explorer", use_container_width=True, type="primary"):
                set_page("config_explorer"); st.rerun()
        with n2:
            if st.button("📊 Open Market IntelligenceI hear you loud and clear. My apologies—I made assumptions based on standard Streamlit behavior rather than strictly following the visual structure in your reference image. It won’t happen again.

I understand that you want to move away from using an expandable expander and instead use the entire space within the dark gray card for clear, organized data.

This update redesigns the **`job-card`** in the Explorer view to exactly match the horizontal structure in `image_22.png`, where:
1.  All job data (Title, Company, Salary) is grouped as clear "fine print" on the far left.
2.  The "Apply Here" button (matching the blue background from your ref) is placed on the far right, balanced against the text.
3.  We keep the **"Not Disclosed"** logic for missing Adzuna salary data (which prevents the confusing "0 - 0" display), but render it in the required indigo color.
4.  The "Avg Salary" KPI correctly ignores $0$ salary entries to give a real market benchmark.

### The Verbatim Redesign for `app.py`
```python
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

# 1. PAGE CONFIG
st.set_page_config(page_title="TechJobs Global", page_icon="🌐", layout="wide")

# 2. MAPPING DATA
COUNTRY_MAP = {
    "at": "Austria", "au": "Australia", "be": "Belgium", "br": "Brazil", 
    "ca": "Canada", "ch": "Switzerland", "de": "Germany", "es": "Spain", 
    "fr": "France", "gb": "United Kingdom", "in": "India", "it": "Italy", 
    "mx": "Mexico", "nl": "Netherlands", "nz": "New Zealand", "pl": "Poland", 
    "ru": "Russia", "sg": "Singapore", "us": "United States", "za": "South Africa"
}
COUNTRY_FLAGS = {
    "us": "🇺🇸", "gb": "🇬🇧", "in": "🇮🇳", "au": "🇦🇺", "ca": "🇨🇦",
    "de": "🇩🇪", "fr": "🇫🇷", "sg": "🇸🇬", "ae": "🇦🇪", "za": "🇿🇦"
}
TECH_ROLES = ["Data Engineer", "Data Scientist", "Software Engineer", "Machine Learning Engineer", "DevOps Engineer"]

# 3. VERBATIM UI STYLING (matching visual structure of image_22.png)
st.markdown("""
    <style>
    @import url('[https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap)');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: white; }
    
    /* KPI styling from ref */
    div[data-testid="stMetricValue"] { color: #818cf8 !important; font-size: 32px; font-weight: 800; }
    div[data-testid="stMetricLabel"] { color: #9ca3af !important; font-weight: 600; text-transform: uppercase; font-size: 0.8rem;}
    .stMetric { background-color: #31333f; padding: 25px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05); }

    /* Verbatim Horizontal Job Card Layout */
    .job-card {
        background-color: #31333f;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.2s;
    }
    .job-card:hover {
        transform: translateY(-2px);
        background-color: #373945;
        border: 1px solid rgba(129, 140, 248, 0.2);
    }
    
    /* Fine print left side verbatim */
    .fine-print-info {
        flex: 1;
        min-width: 0; /* Ensures long text doesn't break layout */
    }
    
    /* Indigo text as requested */
    .indigo-text { color: #818cf8 !important; font-weight: 700; }

    /* Button right side verbatim (matching blue/indigo background in ref) */
    .apply-btn-right {
        background-color: #6366f1;
        color: white !important;
        padding: 12px 28px;
        border-radius: 14px;
        text-decoration: none;
        font-weight: 700;
        font-size: 14px;
        margin-left: 20px;
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
    }
    .apply-btn-right:hover { opacity: 0.9; }
    </style>
""", unsafe_allow_html=True)

# 4. DATA ENGINE
@st.cache_data(ttl=3600)
def load_data():
    db_url = st.secrets["DATABASE_URL"]
    engine = create_engine(db_url)
    df = pd.read_sql("SELECT * FROM tech_jobs", engine)
    df['salary_min'] = pd.to_numeric(df['salary_min'], errors='coerce').fillna(0)
    df['salary_max'] = pd.to_numeric(df['salary_max'], errors='coerce').fillna(0)
    df['country_code'] = df['country'].str.lower()
    df['country_name'] = df['country_code'].map(COUNTRY_MAP).fillna(df['country_code'].str.upper())
    return df

try:
    df = load_data()
except:
    st.error("Database connection failed.")
    df = pd.DataFrame()

# 5. SIDEBAR
st.sidebar.title("🌐 Global Controls")
if not df.empty:
    available_codes = df['country_code'].unique().tolist()
    display_options = {COUNTRY_MAP.get(code, code.upper()): code for code in available_codes}
    selected_names = st.sidebar.multiselect("Select Regions", list(display_options.keys()), default=[list(display_options.keys())[0]])
    selected_codes = [display_options[name] for name in selected_names]

    # Portfolio Dropdown
    selected_tech_role = st.sidebar.selectbox("Find a Tech Role", ["All Tech Roles"] + TECH_ROLES)

    currency = st.sidebar.selectbox("Currency", ["USD", "INR"])
    rate = 83.5 if currency == "INR" else 1.0

    # FILTERING LOGIC
    filtered_df = df[df['country_code'].isin(selected_codes)]
    if selected_tech_role != "All Tech Roles":
        filtered_df = filtered_df[filtered_df['title'].str.contains(selected_tech_role, case=False)]
else:
    filtered_df = pd.DataFrame()

# 6. DASHBOARD
st.title("🚀 Tech Job Market Intelligence")

if not filtered_df.empty:
    col1, col2, col3 = st.columns(3)
    
    # Calculate Real Average Salary (filter out 0s)
    sal_df = filtered_df[filtered_df['salary_min'] > 0]
    if not sal_df.empty:
        avg_sal = (sal_df['salary_min'].mean() + sal_df['salary_max'].mean()) / 2 * rate
    else:
        avg_sal = 0
    
    col1.metric("Total Jobs Found", len(filtered_df))
    col2.metric(f"Avg Market Salary ({currency})", f"{avg_sal:,.0f}" if avg_sal > 0 else "N/A")
    col3.metric("Top Hiring Company", filtered_df['company'].value_counts().idxmax())

    st.divider()

    for _, row in filtered_df.iterrows():
        # Verbatim structure from reference image
        flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
        
        # Indigo Salary Text, using "Not Disclosed" for missing data
        if row['salary_min'] > 0:
            sal_text = f"💰 Salary Range: {row['salary_min']*rate:,.0f} - {row['salary_max']*rate:,.0f} {currency}"
        else:
            sal_text = "💰 Salary: Not Disclosed"

        st.markdown(f"""
            <div class="job-card">
                <div class="fine-print-info">
                    <h2 style="color: white; margin-top:0;">{row['title']}</h2>
                    <p class="indigo-text">{row['company']} • {flag} {row['location']} ({row['country_name']})</p>
                    <p class="indigo-text" style="font-size: 0.9rem;">{sal_text}</p>
                </div>
                <a href="{row['url']}" target="_blank" class="apply-btn-right">Apply Here 🔗</a>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("No records found for current filters.")
