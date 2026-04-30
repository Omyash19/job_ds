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
    "us": "🇺🇸", "gb": "🇬🇧", "in": "🇮🇳", "au": "🇦🇺", "ca": "🇨🇦",
    "de": "🇩🇪", "fr": "🇫🇷", "sg": "🇸🇬", "ae": "🇦🇪", "za": "🇿🇦"
}
TECH_ROLES = ["Data Engineer", "Data Scientist", "Data Analyst", "Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Machine Learning Engineer", "DevOps Engineer"]
SKILL_KEYWORDS = ["Python", "SQL", "AWS", "Azure", "Docker", "Kubernetes", "Spark", "React", "Tableau", "Snowflake", "Java"]

# 3. VERBATIM UI STYLING
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: white; }
    
    /* Dark Theme Background */
    .main { background: #0c0e12; }
    
    /* Completely Hide Sidebar in Features */
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none; }

    /* Landing Hero */
    .hero-title { text-align: center; color: white; font-weight: 800; font-size: 4.5rem; margin-top: 100px; }
    .hero-subtitle { text-align: center; color: #818cf8; font-size: 1.3rem; margin-bottom: 60px; }
    
    /* Configuration Box */
    .config-box {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 50px;
        border-radius: 30px;
        max-width: 850px;
        margin: 0 auto;
    }

    /* Horizontal Card Structure (Verbatim from image_c64a98.png) */
    .job-card {
        background: #1e2028;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.2s ease;
    }
    .job-card:hover {
        transform: translateY(-3px);
        background: #252731;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    .fine-print-left { flex: 1; min-width: 0; }
    .indigo-label { color: #818cf8; font-weight: 700; font-size: 1rem; margin-bottom: 5px; }
    .salary-tag { color: #64748b; font-size: 0.9rem; font-weight: 400; }

    /* Blue Apply Button (Right Aligned) */
    .apply-btn {
        background-color: #6366f1;
        color: white !important;
        padding: 12px 28px;
        border-radius: 14px;
        text-decoration: none;
        font-weight: 700;
        font-size: 14px;
        white-space: nowrap;
        margin-left: 20px;
    }
    
    .desc-text { color: #9ca3af; font-size: 1.1rem; line-height: 1.7; margin-bottom: 50px; padding: 20px; border-left: 4px solid #6366f1; background: rgba(255,255,255,0.02); }
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

# 5. NAVIGATION STATE
if 'page' not in st.session_state: st.session_state.page = "landing"
if 'filters' not in st.session_state: st.session_state.filters = {}

# 6. APP CONTENT
if not raw_df.empty:
    
    # ─── VIEW 1: LANDING ───
    if st.session_state.page == "landing":
        st.markdown('<h1 class="hero-title">ECHOES 💎</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">The Intelligence Layer for the Global Tech Economy</p>', unsafe_allow_html=True)
        
        c_l, c1, c2, c_r = st.columns([1, 2, 2, 1])
        with c1:
            if st.button("🔍 Launch Job Explorer", use_container_width=True, type="primary"):
                st.session_state.page = "config_explorer"; st.rerun()
        with c2:
            if st.button("📊 Market Intelligence", use_container_width=True):
                st.session_state.page = "config_analytics"; st.rerun()

    # ─── VIEW 2: CONFIGURATION ───
    elif st.session_state.page in ["config_explorer", "config_analytics"]:
        st.markdown('<h1 style="text-align:center; color:white; margin-top:50px;">Configure Your Insight</h1>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="config-box">', unsafe_allow_html=True)
            available_countries = sorted(raw_df['country_name'].unique().tolist())
            col_a, col_b = st.columns(2)
            with col_a:
                sel_regions = st.multiselect("Select Regions", available_countries, default=available_countries[:1])
            with col_b:
                sel_currency = st.radio("Display Currency", ["USD", "INR"], horizontal=True)
            
            sel_role = "All Roles"
            if st.session_state.page == "config_explorer":
                sel_role = st.selectbox("Target Tech Stack", TECH_ROLES)
            
            st.write("---")
            btn_label = "Search Live Market" if st.session_state.page == "config_explorer" else "Generate Market Report"
            if st.button(btn_label, use_container_width=True, type="primary"):
                st.session_state.filters = {"regions": sel_regions, "currency": sel_currency, "role": sel_role, "rate": 83.5 if sel_currency == "INR" else 1.0}
                st.session_state.page = "results_explorer" if st.session_state.page == "config_explorer" else "results_analytics"
                st.rerun()
            if st.button("← Back to Home"): st.session_state.page = "landing"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ─── VIEW 3: RESULTS (Explorer) ───
    elif st.session_state.page == "results_explorer":
        f = st.session_state.filters
        st.markdown(f"## 🔍 Explorer: {f['role']} in {', '.join(f['regions'])}")
        if st.button("Adjust Filters"): st.session_state.page = "config_explorer"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        if f['role'] != "All Roles":
            res_df = res_df[res_df['title'].str.contains(f['role'], case=False)]
        
        if not res_df.empty:
            st.markdown("### ✨ Premium Matches")
            top_3 = res_df.sort_values(by='salary_max', ascending=False).head(3)
            for _, row in top_3.iterrows():
                flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
                sal = f"{row['salary_min']*f['rate']:,.0f} - {row['salary_max']*f['rate']:,.0f} {f['currency']}" if row['salary_min'] > 0 else "Not Disclosed"
                st.markdown(f"""
                    <div class="job-card">
                        <div class="fine-print-left">
                            <h2 style="margin:0; font-size:1.6rem; color:white;">{row['title']} <small style="font-size:12px; color:#818cf8;">(TOP MATCH)</small></h2>
                            <p class="indigo-label">{row['company']} • {flag} {row['location']} ({row['country_name']})</p>
                            <p class="salary-tag">💰 Benchmark Salary: {sal}</p>
                        </div>
                        <a href="{row['url']}" target="_blank" class="apply-btn">Apply Now</a>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            for _, row in res_df.iloc[3:].iterrows():
                st.markdown(f"""
                    <div class="job-card">
                        <div class="fine-print-left">
                            <h3 style="margin:0; color:white;">{row['title']}</h3>
                            <p class="indigo-label">{row['company']} • {row['location']}</p>
                        </div>
                        <a href="{row['url']}" target="_blank" class="apply-btn" style="padding:10px 20px;">Apply</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No records match your current filters.")

    # ─── VIEW 3: RESULTS (Analytics) ───
    elif st.session_state.page == "results_analytics":
        f = st.session_state.filters
        st.markdown(f"## 📊 Market Report: {', '.join(f['regions'])}")
        if st.button("Adjust Parameters"): st.session_state.page = "config_analytics"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        
        # Salary Box Plot
        st.markdown("#### 💸 Salary Variance by Region")
        sal_clean = res_df[res_df['salary_min'] > 0]
        if not sal_clean.empty:
            fig1 = px.box(sal_clean, x="country_name", y="salary_min", color="country_name", template="plotly_dark", labels={"salary_min": f"Salary ({f['currency']})", "country_name": "Region"})
            fig1.update_traces(hovertemplate="<b>%{x}</b><br>Salary: %{y}<extra></extra>")
            fig1.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('<div class="desc-text">This diagram illustrates the salary variance across your selected regions. The central box represents the middle 50% of the market, while high-value dots indicate specialized roles with higher premiums.</div>', unsafe_allow_html=True)

else:
    st.error("Engine failure. Please check your Supabase secrets.")
