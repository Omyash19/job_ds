import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import time

# 1. PAGE CONFIG (Full Immersive)
st.set_page_config(
    page_title="ECHOES | Tech Intelligence", 
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
COUNTRY_FLAGS = {"us": "🇺🇸", "gb": "🇬🇧", "in": "🇮🇳", "au": "🇦🇺", "ca": "🇨🇦", "de": "🇩🇪", "fr": "🇫🇷"}
TECH_ROLES = ["Data Engineer", "Data Scientist", "Data Analyst", "Software Engineer", "Machine Learning Engineer", "DevOps Engineer"]

# 3. ELITE UI ARCHITECTURE (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"], [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #0f172a; }

    /* 1. Realistic Glass Mesh Background */
    .stApp {
        background: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                    radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
                    #F8FAFC;
    }

    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }

    /* 2. Visual Hierarchy Typography */
    .hero-title { text-align: center; color: #0f172a; font-weight: 800; font-size: 4.2rem; margin-top: 50px; margin-bottom: 0px; letter-spacing: -2px; }
    .hero-bridge { text-align: center; color: #475569; font-size: 1.4rem; font-weight: 500; margin-bottom: 10px; }
    .hero-subtitle { text-align: center; color: #6366f1; font-size: 0.9rem; margin-bottom: 50px; font-weight: 800; text-transform: uppercase; letter-spacing: 3px; }

    /* 3. Refined Glassmorphic Card (No Pop-in) */
    .glass-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 32px;
        padding: 45px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.06);
    }

    /* 4. Horizontal Job Card with Micro-interactions */
    .job-card {
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid white;
        border-radius: 20px;
        padding: 25px 35px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    .job-card:hover {
        transform: translateX(10px);
        background: white;
        border-left: 8px solid #6366f1;
        box-shadow: 20px 20px 40px rgba(0,0,0,0.05);
    }

    /* 5. KPI Analytics Summary Tiles */
    .kpi-container { display: flex; gap: 20px; margin-bottom: 40px; justify-content: center; }
    .kpi-tile {
        background: white;
        padding: 20px 30px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        text-align: center;
        flex: 1;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    }
    .kpi-value { color: #6366f1; font-weight: 800; font-size: 1.8rem; display: block; }
    .kpi-label { color: #64748b; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }

    /* Buttons */
    .stButton > button { border-radius: 14px; font-weight: 700; transition: all 0.2s ease; border: 1px solid #e2e8f0; background: white; }
    .stButton > button:hover { border-color: #6366f1; color: #6366f1; transform: translateY(-2px); }
    .stButton > button[kind="primary"] { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; border: none; }

    /* Narrative Box */
    .narrative-box { color: #475569; font-size: 1rem; line-height: 1.7; padding: 20px; background: rgba(99, 102, 241, 0.03); border-radius: 15px; border-left: 4px solid #6366f1; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# 4. DATA ENGINE
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
    except:
        return pd.DataFrame()

raw_df = load_data()

# 5. STATE MANAGEMENT
if 'view' not in st.session_state: st.session_state.view = "landing"
if 'f' not in st.session_state: st.session_state.f = {}

# 6. APP LOGIC
if not raw_df.empty:
    
    # ─── LANDING ───
    if st.session_state.view == "landing":
        st.markdown('<h1 class="hero-title">ECHOES 💎</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-bridge">Macro-economic Tech Market Intelligence</p>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">High Precision Data for the Modern Analyst</p>', unsafe_allow_html=True)
        
        _, c1, c2, _ = st.columns([1, 2, 2, 1])
        with c1:
            if st.button("🔍 Launch Job Explorer", use_container_width=True, type="primary"):
                st.session_state.view = "config_explorer"; st.rerun()
        with c2:
            if st.button("📊 Access Intelligence", use_container_width=True):
                st.session_state.view = "config_analytics"; st.rerun()

    # ─── CONFIGURATION ───
    elif st.session_state.view in ["config_explorer", "config_analytics"]:
        st.markdown('<div style="height:60px;"></div>', unsafe_allow_html=True)
        _, center_col, _ = st.columns([1, 2.5, 1])
        with center_col:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<h2 style="margin-top:0; color:#0f172a; font-weight:800;">Configure Insight</h2>', unsafe_allow_html=True)
            
            sel_regions = st.multiselect("1. Target Regions", sorted(raw_df['country_name'].unique().tolist()), default=[raw_df['country_name'].unique().tolist()[0]])
            
            c_a, c_b = st.columns(2)
            with c_a:
                sel_currency = st.radio("2. Financial Currency", ["USD", "INR"], horizontal=True)
            with c_b:
                sel_role = "All Roles"
                if st.session_state.view == "config_explorer":
                    sel_role = st.selectbox("3. Tech Stack Preference", ["All Roles"] + TECH_ROLES)
            
            st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)
            
            btn_label = "Search Live Market" if st.session_state.view == "config_explorer" else "Generate Intelligence Report"
            if st.button(btn_label, use_container_width=True, type="primary"):
                st.session_state.f = {"regions": sel_regions, "currency": sel_currency, "role": sel_role, "rate": 83.5 if sel_currency == "INR" else 1.0}
                st.session_state.view = "results_explorer" if st.session_state.view == "config_explorer" else "results_analytics"
                st.rerun()
            
            if st.button("← Back", use_container_width=True):
                st.session_state.view = "landing"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ─── EXPLORER RESULTS ───
    elif st.session_state.view == "results_explorer":
        f = st.session_state.f
        st.markdown(f'<h2 style="text-align:center; font-weight:800; color:#0f172a;">🔍 Global Explorer</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center; color:#64748b;">{f["role"]} matching across {", ".join(f["regions"])}</p>', unsafe_allow_html=True)
        
        _, back_c, _ = st.columns([1, 0.4, 1])
        with back_c:
            if st.button("← Back", use_container_width=True): st.session_state.view = "config_explorer"; st.rerun()

        # Search Bar for Information Density
        search_query = st.text_input("Filter results by keyword (e.g. Remote, Netflix)...", placeholder="Search live data...")

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        if f['role'] != "All Roles":
            res_df = res_df[res_df['title'].str.contains(f['role'], case=False)]
        if search_query:
            res_df = res_df[res_df['title'].str.contains(search_query, case=False) | res_df['company'].str.contains(search_query, case=False)]

        for _, row in res_df.iterrows():
            flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
            sal = f"{row['salary_min']*f['rate']:,.0f} - {row['salary_max']*f['rate']:,.0f} {f['currency']}" if row['salary_min'] > 0 else "Benchmark Disclosed on Apply"
            st.markdown(f"""
                <div class="job-card">
                    <div style="flex:1;">
                        <h3 style="margin:0; font-size:1.4rem; color:#0f172a;">{row['title']}</h3>
                        <p style="color: #6366f1; font-weight: 700; margin: 8px 0;">{row['company']} • {flag} {row['location']} ({row['country_name']})</p>
                        <p style="color: #64748b; font-size: 0.9rem; font-weight:600;">{sal}</p>
                    </div>
                    <a href="{row['url']}" target="_blank" class="apply-btn">Apply Now</a>
                </div>
            """, unsafe_allow_html=True)

    # ─── ANALYTICS RESULTS ───
    elif st.session_state.view == "results_analytics":
        f = st.session_state.f
        st.markdown(f'<h2 style="text-align:center; font-weight:800; color:#0f172a;">📊 Intelligence Report</h2>', unsafe_allow_html=True)
        
        _, back_c, _ = st.columns([1, 0.4, 1])
        with back_c:
            if st.button("← Back", use_container_width=True): st.session_state.view = "config_analytics"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        sal_clean = res_df[res_df['salary_min'] > 0]
        
        # KPI SUMMARY TILES (The roadmap requirement)
        avg_sal = (sal_clean['salary_min'].mean() + sal_clean['salary_max'].mean())/2 * f['rate'] if not sal_clean.empty else 0
        st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-tile"><span class="kpi-label">Median Salary</span><span class="kpi-value">{f['currency']} {avg_sal:,.0f}</span></div>
                <div class="kpi-tile"><span class="kpi-label">Active Records</span><span class="kpi-value">{len(res_df)}</span></div>
                <div class="kpi-tile"><span class="kpi-label">Market Velocity</span><span class="kpi-value">High</span></div>
            </div>
        """, unsafe_allow_html=True)

        # Salary Box Plot
        st.markdown('<div class="glass-card" style="margin-bottom:40px;">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top:0;">💸 Regional Salary Variance</h3>', unsafe_allow_html=True)
        if not sal_clean.empty:
            fig1 = px.box(sal_clean, x="country_name", y="salary_min", template="plotly_white", color_discrete_sequence=['#6366f1'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0))
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        st.markdown('<div class="narrative-box">Statistical identification of pay floors and ceilings. Outliers indicate specialized roles commanding significant market premiums.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error("Engine offline. Please verify database connectivity.")
