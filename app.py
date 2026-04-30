import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# 1. PAGE CONFIG (Zero-Sidebar Immersive Mode)
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

# 3. HIGH-END GLASSMORPHISM CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #1e293b; }
    
    /* Light Airy Background */
    .main { background: #f8fafc; }
    
    /* Completely Hide Sidebar */
    [data-testid="stSidebar"] { display: none; }

    /* Hero Branding */
    .hero-title { text-align: center; color: #0f172a; font-weight: 800; font-size: 3.5rem; margin-top: 60px; }
    .hero-subtitle { text-align: center; color: #6366f1; font-size: 1.1rem; margin-bottom: 50px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Config Box (Glassmorphic) */
    .config-box {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        padding: 40px;
        border-radius: 32px;
        max-width: 900px;
        margin: 0 auto;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05);
    }

    /* KPI Cards (Glassmorphic) */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        padding: 25px;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    }
    div[data-testid="stMetricValue"] { color: #0f172a !important; font-weight: 800 !important; }
    div[data-testid="stMetricLabel"] { color: #64748b !important; font-weight: 700 !important; text-transform: uppercase; font-size: 0.8rem; }

    /* Horizontal Glass Job Card */
    .job-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        padding: 25px 35px;
        border-radius: 28px;
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.02);
    }
    .job-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 40px rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    .match-tag {
        background: #f1f5f9;
        color: #6366f1;
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    /* Premium Purple Button */
    .apply-btn {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white !important;
        padding: 12px 28px;
        border-radius: 16px;
        text-decoration: none;
        font-weight: 700;
        font-size: 14px;
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
        transition: opacity 0.2s;
    }
    .apply-btn:hover { opacity: 0.9; }

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

# 6. APP CONTENT
if not raw_df.empty:
    
    # ─── VIEW 1: LANDING ───
    if st.session_state.page == "landing":
        st.markdown('<h1 class="hero-title">ECHOES 💎</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">Intelligence for the Tech Economy</p>', unsafe_allow_html=True)
        
        c_l, c1, c2, c_r = st.columns([1, 2, 2, 1])
        with c1:
            if st.button("🔍 Launch Job Explorer", use_container_width=True, type="primary"):
                st.session_state.page = "config_explorer"; st.rerun()
        with c2:
            if st.button("📊 Market Intelligence", use_container_width=True):
                st.session_state.page = "config_analytics"; st.rerun()

    # ─── VIEW 2: CONFIG ───
    elif st.session_state.page in ["config_explorer", "config_analytics"]:
        st.markdown('<h2 style="text-align:center; margin-top:50px;">Configure Your Insight</h2>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="config-box">', unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                sel_regions = st.multiselect("Select Regions", sorted(raw_df['country_name'].unique().tolist()), default=[raw_df['country_name'].unique().tolist()[0]])
            with col_b:
                sel_currency = st.radio("Display Currency", ["USD", "INR"], horizontal=True)
            
            sel_role = "All Roles"
            if st.session_state.page == "config_explorer":
                sel_role = st.selectbox("Define Your Target Tech Stack", TECH_ROLES)
            
            st.divider()
            if st.button("Generate Experience", use_container_width=True, type="primary"):
                st.session_state.filters = {"regions": sel_regions, "currency": sel_currency, "role": sel_role, "rate": 83.5 if sel_currency == "INR" else 1.0}
                st.session_state.page = "results_explorer" if st.session_state.page == "config_explorer" else "results_analytics"
                st.rerun()
            if st.button("← Cancel"): st.session_state.page = "landing"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ─── VIEW 3: RESULTS (Explorer) ───
    elif st.session_state.page == "results_explorer":
        f = st.session_state.filters
        st.markdown(f"### 🔍 Explorer: {f['role']} in {', '.join(f['regions'])}")
        if st.button("Adjust Filters", type="secondary"): st.session_state.page = "config_explorer"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        if f['role'] != "All Roles":
            res_df = res_df[res_df['title'].str.contains(f['role'], case=False)]
        
        if not res_df.empty:
            st.markdown("#### ✨ Premium Matches")
            top_3 = res_df.sort_values(by='salary_max', ascending=False).head(3)
            for _, row in top_3.iterrows():
                flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
                sal = f"{row['salary_min']*f['rate']:,.0f} - {row['salary_max']*f['rate']:,.0f} {f['currency']}" if row['salary_min'] > 0 else "Not Disclosed"
                st.markdown(f"""
                    <div class="job-card">
                        <div style="flex:1;">
                            <h2 style="margin:0; font-size:1.6rem;">{row['title']} <span class="match-tag">TOP MATCH</span></h2>
                            <p style="color: #6366f1; font-weight: 700; margin: 8px 0;">{row['company']} • {flag} {row['location']} ({row['country_name']})</p>
                            <p style="color: #64748b; font-size: 0.9rem;">💰 <b>Benchmark Salary:</b> {sal}</p>
                        </div>
                        <a href="{row['url']}" target="_blank" class="apply-btn">Apply Now</a>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            st.markdown(f"#### Global Tech Hub Opportunities")
            for _, row in res_df.iloc[3:].iterrows():
                flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
                st.markdown(f"""
                    <div class="job-card" style="padding: 20px 30px;">
                        <div style="flex:1;">
                            <h3 style="margin:0;">{row['title']}</h3>
                            <p style="color: #64748b; font-size: 0.9rem;">{row['company']} • {flag} {row['location']}</p>
                        </div>
                        <a href="{row['url']}" target="_blank" class="apply-btn" style="padding:8px 20px; font-size:12px;">View Role</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Scanning... No matches currently found.")

    # ─── VIEW 3: RESULTS (Analytics) ───
    elif st.session_state.page == "results_analytics":
        f = st.session_state.filters
        st.markdown(f"### 📊 Intelligence Report: {', '.join(f['regions'])}")
        if st.button("Adjust Parameters"): st.session_state.page = "config_analytics"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        
        # Dashboard Layout
        c1, c2, c3 = st.columns(3)
        sal_clean = res_df[res_df['salary_min'] > 0]
        avg = (sal_clean['salary_min'].mean() + sal_clean['salary_max'].mean()) / 2 * f['rate'] if not sal_clean.empty else 0
        c1.metric("Live Sample", f"{len(res_df)} Jobs")
        c2.metric(f"Market Avg ({f['currency']})", f"{avg:,.0f}" if avg > 0 else "N/A")
        c3.metric("Top Employer", res_df['company'].value_counts().idxmax() if not res_df.empty else "N/A")

        st.markdown("#### 💸 Salary Benchmarking")
        fig1 = px.box(sal_clean, x="country_name", y="salary_min", template="plotly_white", color_discrete_sequence=['#6366f1'])
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('<div class="desc-box">Comparative analysis of regional pay scales. High whiskers indicate advanced specialization premiums in these hubs.</div>', unsafe_allow_html=True)

else:
    st.error("Engine Connection Failure.")
