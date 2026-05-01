import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# 1. PAGE CONFIG (Full Immersive, Zero-Sidebar)
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

# 3. CONSOLIDATED ELITE CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #1e293b; }
    
    .main { background: #f1f5f9; }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none; }

    /* Header & Navigation Styling */
    .header-container { text-align: center; margin-top: 40px; margin-bottom: 50px; width: 100%; }
    .header-title { color: #0f172a; font-weight: 800; font-size: 3.5rem; margin-bottom: 0px; }
    .header-subtitle { color: #6366f1; font-weight: 700; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 2px; }

    /* Modular Section Card */
    .report-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-top: 6px solid #6366f1;
        padding: 40px;
        border-radius: 28px;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }
    
    /* Horizontal Job Card (Fine Print Left, Button Right) */
    .job-card {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 30px 40px;
        border-radius: 24px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
    }
    .job-card:hover { transform: translateY(-4px); box-shadow: 0 15px 40px rgba(99, 102, 241, 0.1); border: 1px solid #6366f1; }
    .premium-card { border-left: 6px solid #6366f1; }

    .apply-btn {
        background: #6366f1;
        color: white !important;
        padding: 12px 28px;
        border-radius: 14px;
        text-decoration: none;
        font-weight: 700;
        font-size: 14px;
        white-space: nowrap;
    }

    .report-title { color: #0f172a; font-weight: 800; font-size: 1.8rem; margin-bottom: 25px; }
    .narrative-box { color: #475569; font-size: 1.05rem; line-height: 1.7; padding: 20px 25px; background: #f8fafc; border-radius: 16px; border-left: 5px solid #6366f1; margin-top: 25px; }
    .stButton > button { border-radius: 12px; font-weight: 700; }
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
if 'view' not in st.session_state: st.session_state.view = "landing"
if 'f' not in st.session_state: st.session_state.f = {}

# 6. APP CONTENT
if not raw_df.empty:
    
    # ─── VIEW 1: LANDING ───
    if st.session_state.view == "landing":
        st.markdown('<div class="header-container"><h1 class="header-title">ECHOES 💎</h1><p class="header-subtitle">Intelligence for the Tech Economy</p></div>', unsafe_allow_html=True)
        _, c1, c2, _ = st.columns([1, 2, 2, 1])
        with c1:
            if st.button("🔍 Launch Job Explorer", use_container_width=True, type="primary"):
                st.session_state.view = "config_explorer"; st.rerun()
        with c2:
            if st.button("📊 Market Intelligence", use_container_width=True):
                st.session_state.view = "config_analytics"; st.rerun()

    # ─── VIEW 2: CONFIGURATION ───
    elif st.session_state.view in ["config_explorer", "config_analytics"]:
        st.markdown('<div class="header-container"><h1 class="header-title">Configure Insight</h1></div>', unsafe_allow_html=True)
        _, center_col, _ = st.columns([1, 2.5, 1])
        with center_col:
            st.markdown('<div style="background:white; padding:40px; border-radius:24px; box-shadow:0 4px 20px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                sel_regions = st.multiselect("Select Regions", sorted(raw_df['country_name'].unique().tolist()), default=[raw_df['country_name'].unique().tolist()[0]])
            with c2:
                sel_currency = st.radio("Display Currency", ["USD", "INR"], horizontal=True)
            
            sel_role = "All Roles"
            if st.session_state.view == "config_explorer":
                sel_role = st.selectbox("Define Tech Stack", TECH_ROLES)
            
            st.write("---")
            if st.button("Generate Experience", use_container_width=True, type="primary"):
                st.session_state.f = {"regions": sel_regions, "currency": sel_currency, "role": sel_role, "rate": 83.5 if sel_currency == "INR" else 1.0}
                st.session_state.view = "results_explorer" if st.session_state.view == "config_explorer" else "results_analytics"
                st.rerun()
            if st.button("← Back", use_container_width=True):
                st.session_state.view = "landing"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ─── VIEW 3: EXPLORER (Restored logic) ───
    elif st.session_state.view == "results_explorer":
        f = st.session_state.f
        st.markdown(f'<div class="header-container"><h1 class="header-title">🔍 Global Explorer</h1><p class="header-subtitle">{f["role"]} matches for {", ".join(f["regions"])}</p></div>', unsafe_allow_html=True)
        
        _, back_col, _ = st.columns([1, 0.4, 1])
        with back_col:
            if st.button("← Back", use_container_width=True): st.session_state.view = "config_explorer"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        if f['role'] != "All Roles":
            res_df = res_df[res_df['title'].str.contains(f['role'], case=False)]
        
        if not res_df.empty:
            for _, row in res_df.iterrows():
                flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
                sal = f"{row['salary_min']*f['rate']:,.0f} - {row['salary_max']*f['rate']:,.0f} {f['currency']}" if row['salary_min'] > 0 else "Competitive Market Rate"
                st.markdown(f"""
                    <div class="job-card">
                        <div style="flex:1;">
                            <h2 style="margin:0; font-size:1.6rem; color:#0f172a;">{row['title']}</h2>
                            <p style="color: #6366f1; font-weight: 700; margin: 8px 0; font-size:1rem;">{row['company']} • {flag} {row['location']} ({row['country_name']})</p>
                            <p style="color: #64748b; font-size: 0.9rem; font-weight:600;">💰 Benchmark Salary: {sal}</p>
                        </div>
                        <a href="{row['url']}" target="_blank" class="apply-btn">Apply Here</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No records found for this configuration.")

    # ─── VIEW 4: ANALYTICS (Modular Sections) ───
    elif st.session_state.view == "results_analytics":
        f = st.session_state.f
        st.markdown(f'<div class="header-container"><h1 class="header-title">📊 Intelligence Report</h1><p class="header-subtitle">Analyzing Trends for {", ".join(f["regions"])}</p></div>', unsafe_allow_html=True)
        
        _, back_col, _ = st.columns([1, 0.4, 1])
        with back_col:
            if st.button("← Back", use_container_width=True): st.session_state.view = "config_analytics"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        sal_clean = res_df[res_df['salary_min'] > 0]
        
        # Section 1: Salary
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.markdown('<div class="report-title">💸 Regional Salary Variance</div>', unsafe_allow_html=True)
        if not sal_clean.empty:
            fig1 = px.box(sal_clean, x="country_name", y="salary_min", template="plotly_white", color_discrete_sequence=['#6366f1'], labels={"salary_min": f"Salary ({f['currency']})", "country_name": "Region"})
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20))
            st.plotly_chart(fig1, use_container_width=True)
        st.markdown('<div class="narrative-box">This visualization identifies the pay floor and ceiling across your selected tech hubs. The central box indicates the market median, while dots represent specialized roles that command significant market premiums.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Section 2: Market Share
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.markdown('<div class="report-title">📈 Global Market Share</div>', unsafe_allow_html=True)
        fig2 = px.pie(res_df, names="country_name", hole=0.6, template="plotly_white", color_discrete_sequence=px.colors.sequential.Purples)
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="narrative-box">This chart analyzes job vacancy density. High-percentage regions represent the most active tech economies, suggesting more liquid hiring conditions and a higher probability of successful placement.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error("Engine offline. Check Supabase connection.")
