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

# 3. ADVANCED UI FINISHING (CSS) - Removed redundant blocks and cleaned up spacing
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: white; }
    
    /* Solid Background to match your environment */
    .main { background: #0c0e12; }
    [data-testid="stSidebar"] { display: none; }

    /* Titles & Headings */
    .hero-title { text-align: center; color: white; font-weight: 800; font-size: 4rem; margin-top: 50px; margin-bottom: 5px; }
    .hero-subtitle { text-align: center; color: #818cf8; font-size: 1.1rem; margin-bottom: 40px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; }
    .section-header { text-align: center; color: white; font-weight: 800; font-size: 2.2rem; margin-bottom: 20px; }

    /* Horizontal Glass Job Card */
    .job-card {
        background: #1e2028;
        padding: 25px 35px;
        border-radius: 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    .job-card:hover { transform: translateY(-4px); border: 1px solid rgba(129, 140, 248, 0.3); background: #252731; }
    
    .apply-btn {
        background: #6366f1;
        color: white !important;
        padding: 12px 30px;
        border-radius: 14px;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    .desc-box { color: #9ca3af; font-size: 1rem; line-height: 1.7; padding: 25px; background: rgba(255,255,255,0.02); border-radius: 20px; margin-bottom: 40px; border: 1px solid rgba(255,255,255,0.05); }
    
    /* Standardizing Button Styles */
    .stButton > button { border-radius: 12px; font-weight: 700; height: 3em; }
    
    /* Fix for the empty block issue: Target the vertical block spacing */
    [data-testid="stVerticalBlock"] > div { gap: 0rem; }
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
    
    # ─── VIEW 1: LANDING PAGE ───
    if st.session_state.page == "landing":
        st.markdown('<h1 class="hero-title">ECHOES 💎</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">The Intelligence Layer for Global Tech</p>', unsafe_allow_html=True)
        
        _, col1, col2, _ = st.columns([1, 2, 2, 1])
        with col1:
            if st.button("🔍 Launch Job Explorer", use_container_width=True, type="primary"):
                st.session_state.page = "config_explorer"; st.rerun()
        with col2:
            if st.button("📊 Market Intelligence", use_container_width=True):
                st.session_state.page = "config_analytics"; st.rerun()

    # ─── VIEW 2: CONFIGURATION PAGE (Cleaned and formatted) ───
    elif st.session_state.page in ["config_explorer", "config_analytics"]:
        st.markdown('<h2 class="section-header">Configure Your Insight</h2>', unsafe_allow_html=True)
        
        # Center aligning using columns
        _, center_col, _ = st.columns([1, 2.5, 1])
        
        with center_col:
            # Row 1: Regions and Currency
            c1, c2 = st.columns(2)
            with c1:
                sel_regions = st.multiselect("Target Regions", sorted(raw_df['country_name'].unique().tolist()), default=[raw_df['country_name'].unique().tolist()[0]])
            with c2:
                sel_currency = st.radio("Financial Currency", ["USD", "INR"], horizontal=True)
            
            # Row 2: Role (Explorer Only)
            sel_role = "All Roles"
            if st.session_state.page == "config_explorer":
                sel_role = st.selectbox("Specify Tech Stack Preference", TECH_ROLES)
            
            st.write("") # Spacing
            
            # Action Buttons
            btn_label = "Search Live Market" if st.session_state.page == "config_explorer" else "Generate Market Report"
            if st.button(btn_label, use_container_width=True, type="primary"):
                st.session_state.filters = {"regions": sel_regions, "currency": sel_currency, "role": sel_role, "rate": 83.5 if sel_currency == "INR" else 1.0}
                st.session_state.page = "results_explorer" if st.session_state.page == "config_explorer" else "results_analytics"
                st.rerun()
            
            # Back Button (Replaces Cancel Journey)
            if st.button("← Back", use_container_width=True):
                st.session_state.page = "landing"; st.rerun()

    # ─── VIEW 3: RESULTS (Explorer) ───
    elif st.session_state.page == "results_explorer":
        f = st.session_state.filters
        st.markdown(f"### 🔍 Explorer: {f['role']} in {', '.join(f['regions'])}")
        if st.button("← Back"): st.session_state.page = "config_explorer"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        if f['role'] != "All Roles":
            res_df = res_df[res_df['title'].str.contains(f['role'], case=False)]
        
        if not res_df.empty:
            st.markdown("#### ✨ Premium Matches")
            top_3 = res_df.sort_values(by='salary_max', ascending=False).head(3)
            for _, row in top_3.iterrows():
                flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
                sal = f"{row['salary_min']*f['rate']:,.0f} - {row['salary_max']*f['rate']:,.0f} {f['currency']}" if row['salary_min'] > 0 else "Competitive Market Rate"
                st.markdown(f"""
                    <div class="job-card">
                        <div style="flex:1;">
                            <h2 style="margin:0; font-size:1.5rem; color:white;">{row['title']}</h2>
                            <p style="color: #818cf8; font-weight: 700; margin: 8px 0; font-size:1rem;">{row['company']} • {flag} {row['location']} ({row['country_name']})</p>
                            <p style="color: #64748b; font-size: 0.9rem; font-weight:600;">Benchmark: {sal}</p>
                        </div>
                        <a href="{row['url']}" target="_blank" class="apply-btn">Apply Now</a>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            for _, row in res_df.iloc[3:].iterrows():
                flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
                st.markdown(f"""
                    <div class="job-card">
                        <div style="flex:1;">
                            <h3 style="margin:0; font-size:1.2rem; color:white;">{row['title']}</h3>
                            <p style="color: #818cf8; font-size: 0.9rem;">{row['company']} • {flag} {row['location']}</p>
                        </div>
                        <a href="{row['url']}" target="_blank" class="apply-btn" style="padding:10px 25px; font-size:0.8rem;">Apply</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No records found for this market segment.")

    # ─── VIEW 3: RESULTS (Analytics) ───
    elif st.session_state.page == "results_analytics":
        f = st.session_state.filters
        st.markdown(f"### 📊 Intelligence Report: {', '.join(f['regions'])}")
        if st.button("← Back"): st.session_state.page = "config_analytics"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        
        k1, k2, k3 = st.columns(3)
        sal_clean = res_df[res_df['salary_min'] > 0]
        avg = (sal_clean['salary_min'].mean() + sal_clean['salary_max'].mean()) / 2 * f['rate'] if not sal_clean.empty else 0
        k1.metric("Live Sample Size", f"{len(res_df)} Roles")
        k2.metric(f"Market Midpoint ({f['currency']})", f"{avg:,.0f}" if avg > 0 else "N/A")
        k3.metric("Top Hiring Hub", res_df['country_name'].value_counts().idxmax() if not res_df.empty else "N/A")

        st.markdown("#### 💸 Salary Benchmarking")
        fig1 = px.box(sal_clean, x="country_name", y="salary_min", template="plotly_dark", color_discrete_sequence=['#6366f1'])
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('<div class="desc-box">Comparative analysis of regional pay scales. Outliers indicate specialized roles with higher market premiums.</div>', unsafe_allow_html=True)

else:
    st.error("Engine failure. Please check your connection.")
                
