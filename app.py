import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go

# 1. PAGE CONFIG
st.set_page_config(page_title="TechJobs Global Pro", page_icon="💎", layout="wide")

# 2. MAPPING & SKILL LOGIC
COUNTRY_MAP = {
    "at": "Austria", "au": "Australia", "be": "Belgium", "br": "Brazil", 
    "ca": "Canada", "ch": "Switzerland", "de": "Germany", "es": "Spain", 
    "fr": "France", "gb": "United Kingdom", "in": "India", "it": "Italy", 
    "mx": "Mexico", "nl": "Netherlands", "nz": "New Zealand", "pl": "Poland", 
    "sg": "Singapore", "us": "United States", "za": "South Africa"
}

TECH_ROLES = ["All Tech Roles", "Data Engineer", "Data Scientist", "Software Engineer", "Machine Learning Engineer", "DevOps Engineer"]

# Common skills to extract for badges
SKILL_KEYWORDS = ["Python", "SQL", "AWS", "Azure", "Docker", "Kubernetes", "Spark", "React", "Tableau", "Power BI", "Snowflake", "Java"]

# 3. ADVANCED GLASSMORPHIC CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Global Background */
    .main {
        background: radial-gradient(circle at top right, #1e1b4b, #020617);
    }

    /* Glassmorphic Metrics */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    div[data-testid="stMetricValue"] { color: #818cf8 !important; font-size: 2.2rem !important; }

    /* Modern Job Card */
    .job-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 24px;
        margin-bottom: 25px;
        transition: all 0.3s ease;
    }
    .job-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(129, 140, 248, 0.3);
        transform: translateY(-5px);
    }

    /* Skill Badges */
    .skill-badge {
        display: inline-block;
        background: rgba(129, 140, 248, 0.1);
        color: #818cf8;
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 8px;
        border: 1px solid rgba(129, 140, 248, 0.2);
    }

    /* Premium Button */
    .apply-btn {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white !important;
        padding: 12px 24px;
        border-radius: 14px;
        text-decoration: none;
        font-weight: 700;
        float: right;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }
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
    df['country'] = df['country'].str.lower()
    return df

try:
    df = load_data()
except:
    st.error("Engine offline. Check DATABASE_URL.")
    df = pd.DataFrame()

# 5. SIDEBAR UPGRADES
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Elite Intelligence")
    
    if not df.empty:
        available_codes = df['country'].unique().tolist()
        display_options = {COUNTRY_MAP.get(code, code.upper()): code for code in available_codes}
        selected_names = st.multiselect("Active Regions", list(display_options.keys()), default=list(display_options.keys())[:2])
        selected_codes = [display_options[name] for name in selected_names]

        selected_tech_role = st.selectbox("Market Segment", TECH_ROLES)
        
        currency = st.radio("Display Currency", ["USD", "INR"], horizontal=True)
        rate = 83.5 if currency == "INR" else 1.0

        # Filtering Logic
        filtered_df = df[df['country'].isin(selected_codes)]
        if selected_tech_role != "All Tech Roles":
            filtered_df = filtered_df[filtered_df['title'].str.contains(selected_tech_role, case=False)]
    else:
        filtered_df = pd.DataFrame()

# 6. MAIN CONTENT
if not filtered_df.empty:
    st.title("💎 Global Market Explorer")
    
    # KPI SECTION
    k1, k2, k3 = st.columns(3)
    sal_df = filtered_df[filtered_df['salary_min'] > 0]
    avg_sal = (sal_df['salary_min'].mean() + sal_df['salary_max'].mean()) / 2 * rate if not sal_df.empty else 0
    
    k1.metric("Live Opportunities", f"{len(filtered_df):,}")
    k2.metric(f"Market Midpoint ({currency})", f"{avg_sal:,.0f}" if avg_sal > 0 else "N/A")
    k3.metric("Lead Employer", filtered_df['company'].value_counts().idxmax())

    # MARKET ANALYTICS UPGRADE
    st.write("### 📊 Salary Distribution by Country")
    fig = px.box(filtered_df[filtered_df['salary_min'] > 0], 
                 x="country", y="salary_min", 
                 points="all", color="country",
                 template="plotly_dark",
                 labels={"salary_min": f"Min Salary ({currency})", "country": "Region"})
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # JOB LISTING UPGRADE
    for _, row in filtered_df.iterrows():
        # Skill Badge Extraction
        found_skills = [s for s in SKILL_KEYWORDS if s.lower() in (row['description'] or "").lower()]
        skill_html = "".join([f'<span class="skill-badge">{s}</span>' for s in found_skills[:5]])
        
        sal_val = f"{row['salary_min']*rate:,.0f} - {row['salary_max']*rate:,.0f} {currency}" if row['salary_min'] > 0 else "Competitive"

        st.markdown(f"""
            <div class="job-card">
                <a href="{row['url']}" target="_blank" class="apply-btn">View Role</a>
                <h2 style="color: white; margin-bottom: 5px;">{row['title']}</h2>
                <p style="color: #818cf8; font-size: 1.1rem; margin-bottom: 15px;">{row['company']} • 📍 {row['location']}</p>
                <div style="margin-bottom: 20px;">{skill_html}</div>
                <p style="color: #9ca3af; font-size: 0.9rem;">💰 <b>Market Rate:</b> {sal_val}</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Explore Intelligence & Requirements"):
            st.markdown(f"### Role Overview")
            st.write(row['description'])
else:
    st.image("https://cdn-icons-png.flaticon.com/512/7486/7486744.png", width=200)
    st.warning("Scanning... No matching data in this sector.")
