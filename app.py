import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

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
SKILL_KEYWORDS = ["Python", "SQL", "AWS", "Azure", "Docker", "Kubernetes", "Spark", "React", "Tableau", "Snowflake", "Java"]

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

    /* Glassmorphism Configuration Card */
    [data-testid="column"] > div[data-testid="stVerticalBlock"]:has(.config-card-marker) {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid white;
        border-radius: 32px;
        padding: 50px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05);
        max-width: 800px;
        margin: 0 auto;
    }

    /* Horizontal Job Card */
    .job-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        padding: 25px 35px;
        border-radius: 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid white;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05);
    }
    
    .apply-btn {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white !important;
        padding: 12px 30px;
        border-radius: 14px;
        text-decoration: none !important;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
    }

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

    .report-card {
        background: white;
        border-top: 6px solid #6366f1;
        padding: 40px;
        border-radius: 24px;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 4. DATA ENGINE (DATABASE RESTORED)
@st.cache_data(ttl=3600)
def load_data():
    try:
        db_url = st.secrets["DATABASE_URL"]
        engine = create_engine(db_url)
        df = pd.read_sql("SELECT * FROM tech_jobs", engine)
        df['salary_min'] = pd.to_numeric(df['salary_min'], errors='coerce').fillna(0)
        df['salary_max'] = pd.to_numeric(df['salary_max'], errors='coerce').fillna(0)
        df['country_code'] = df['country'].str.lower()
        df['country_name'] = df['country_code'].map(COUNTRY_MAP).fillna(df['country_code'].str.upper())
        return df
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return pd.DataFrame()

raw_df = load_data()

# 5. STATE MANAGEMENT
if 'page' not in st.session_state: st.session_state.page = "landing"
if 'filters' not in st.session_state: st.session_state.filters = {}

# 6. APP CONTENT
if not raw_df.empty:
    
    # ─── VIEW 1: LANDING PAGE ───
    if st.session_state.page == "landing":
        st.markdown('<h1 class="hero-title">ECHOES 💎</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">The Intelligence Layer for Global Tech</p>', unsafe_allow_html=True)
        _, center, _ = st.columns([1, 2, 1])
        with center:
            if st.button("Launch Job Explorer", use_container_width=True, type="primary"):
                st.session_state.page = "config_explorer"; st.rerun()
            if st.button("Access Intelligence", use_container_width=True):
                st.session_state.page = "config_analytics"; st.rerun()

    # ─── VIEW 2: CONFIGURATION PAGE ───
    elif st.session_state.page in ["config_explorer", "config_analytics"]:
        st.markdown('<h2 class="section-header">Configure Your Insight</h2>', unsafe_allow_html=True)
        _, center_col, _ = st.columns([1, 4, 1])
        with center_col:
            st.markdown("<div class='config-card-marker'></div>", unsafe_allow_html=True)
            
            # STEP 1: FILTERS (Top)
            st.markdown("<h4 style='margin-top:0; color:#0f172a;'>1. Set Data Parameters</h4>", unsafe_allow_html=True)
            available_countries = sorted(raw_df['country_name'].unique().tolist())
            sel_regions = st.multiselect("Target Regions", available_countries, default=[available_countries[0]])
            
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
                    { "Setting a specific tech stack preference allows ECHOES to filter precision benchmarks." if st.session_state.page == "config_explorer" else "Intelligence reports include regional salary variance and market share." }
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("← Back to Home", use_container_width=True):
                st.session_state.page = "landing"; st.rerun()

    # ─── VIEW 3: RESULTS (Explorer) ───
    elif st.session_state.page == "results_explorer":
        f = st.session_state.filters
        st.markdown(f'<h3 style="text-align:center;">🔍 Explorer: {f["role"]} in {", ".join(f["regions"])}</h3>', unsafe_allow_html=True)
        if st.button("← Back"): st.session_state.page = "config_explorer"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        if f['role'] != "All Roles":
            res_df = res_df[res_df['title'].str.contains(f['role'], case=False)]
        
        for _, row in res_df.iterrows():
            flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
            sal = f"{row['salary_min']*f['rate']:,.0f} - {row['salary_max']*f['rate']:,.0f} {f['currency']}" if row['salary_min'] > 0 else "Competitive Market Rate"
            st.markdown(f"""
                <div class="job-card">
                    <div style="flex:1; text-align: left;">
                        <h2 style="margin:0; font-size:1.5rem; color:#0f172a;">{row['title']}</h2>
                        <p style="color: #6366f1; font-weight: 700; margin: 8px 0; font-size:1rem;">{row['company']} • {flag} {row['location']} ({row['country_name']})</p>
                        <p style="color: #475569; font-size: 0.9rem; font-weight:600; margin:0;">Benchmark: {sal}</p>
                    </div>
                    <a href="{row['url']}" target="_blank" class="apply-btn">Apply Now</a>
                </div>
            """, unsafe_allow_html=True)

    # ─── VIEW 4: RESULTS (Analytics) ───
    elif st.session_state.page == "results_analytics":
        f = st.session_state.filters
        st.markdown(f'<h3 style="text-align:center;">📊 Intelligence Report: {", ".join(f["regions"])}</h3>', unsafe_allow_html=True)
        if st.button("← Back"): st.session_state.page = "config_analytics"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        sal_clean = res_df[res_df['salary_min'] > 0]
        
        # Section 1: Salary Box Plot
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.markdown('<h4>💸 Regional Salary Variance</h4>', unsafe_allow_html=True)
        if not sal_clean.empty:
            fig1 = px.box(sal_clean, x="country_name", y="salary_min", template="plotly_white", color_discrete_sequence=['#6366f1'], labels={"salary_min": f"Salary ({f['currency']})", "country_name": "Region"})
            fig1.update_traces(hovertemplate="<b>%{x}</b><br>Value: %{y:,.1f}<extra></extra>")
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error("Engine offline. Please check your DATABASE_URL in secrets.toml.")
