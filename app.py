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

# 3. ELITE GLASSMORPHIC CSS (Bright Mode)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #1e293b; }
    
    /* Background & Sidebar Hide */
    .main { background: #f8fafc; }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none; }

    /* Hero Branding */
    .hero-title { text-align: center; color: #0f172a; font-weight: 800; font-size: 3.8rem; margin-top: 80px; }
    .hero-subtitle { text-align: center; color: #6366f1; font-size: 1.1rem; margin-bottom: 50px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Glassmorphic Config Card */
    .config-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 1);
        padding: 40px;
        border-radius: 32px;
        width: 100%;
        max-width: 850px;
        margin: 0 auto;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05);
    }

    /* Horizontal Glass Job Card (Verbatim structure) */
    .job-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 1);
        padding: 30px 40px;
        border-radius: 28px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
    }
    .job-card:hover { transform: translateY(-4px); box-shadow: 0 15px 40px rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); }
    
    .premium-highlight { border: 1.5px solid rgba(99, 102, 241, 0.4); background: rgba(255, 255, 255, 0.9); }

    /* Action Button (Right Anchored) */
    .apply-btn {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white !important;
        padding: 12px 30px;
        border-radius: 16px;
        text-decoration: none;
        font-weight: 700;
        font-size: 14px;
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
        white-space: nowrap;
    }

    /* Analytics Narratives */
    .desc-box { color: #475569; font-size: 1rem; line-height: 1.7; padding: 25px; background: white; border-radius: 20px; margin-bottom: 50px; border-left: 5px solid #6366f1; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }
    
    /* Center Aligning Streamlit Buttons */
    .stButton > button { border-radius: 14px; font-weight: 700; height: 3.5em; }
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
    
    # ─── STAGE 1: LANDING ───
    if st.session_state.view == "landing":
        st.markdown('<h1 class="hero-title">ECHOES 💎</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">The Intelligence Layer for the Tech Economy</p>', unsafe_allow_html=True)
        
        _, col1, col2, _ = st.columns([1, 2.2, 2.2, 1])
        with col1:
            if st.button("🔍 Launch Job Explorer", use_container_width=True, type="primary"):
                st.session_state.view = "config_explorer"; st.rerun()
        with col2:
            if st.button("📊 Market Intelligence", use_container_width=True):
                st.session_state.view = "config_analytics"; st.rerun()

    # ─── STAGE 2: CONFIGURATION ───
    elif st.session_state.view in ["config_explorer", "config_analytics"]:
        st.markdown('<h1 style="text-align:center; color:#0f172a; margin-top:60px;">Configure Your Insight</h1>', unsafe_allow_html=True)
        
        _, center_col, _ = st.columns([1, 4, 1])
        with center_col:
            st.markdown('<div class="config-card">', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                sel_regions = st.multiselect("Select Regions", sorted(raw_df['country_name'].unique().tolist()), default=[raw_df['country_name'].unique().tolist()[0]])
            with c2:
                sel_currency = st.radio("Display Currency", ["USD", "INR"], horizontal=True)
            
            sel_role = "All Roles"
            if st.session_state.view == "config_explorer":
                st.write("")
                sel_role = st.selectbox("Define Your Tech Stack", TECH_ROLES)
            
            st.write("---")
            btn_label = "Search Live Market" if st.session_state.view == "config_explorer" else "Generate Report"
            if st.button(btn_label, use_container_width=True, type="primary"):
                st.session_state.f = {"regions": sel_regions, "currency": sel_currency, "role": sel_role, "rate": 83.5 if sel_currency == "INR" else 1.0}
                st.session_state.view = "results_explorer" if st.session_state.view == "config_explorer" else "results_analytics"
                st.rerun()
            
            if st.button("← Back", use_container_width=True):
                st.session_state.view = "landing"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ─── STAGE 3: RESULTS (Explorer) ───
    elif st.session_state.view == "results_explorer":
        f = st.session_state.f
        st.markdown(f"### 🔍 Explorer: {f['role']} in {', '.join(f['regions'])}")
        if st.button("← Back"): st.session_state.view = "config_explorer"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        if f['role'] != "All Roles":
            res_df = res_df[res_df['title'].str.contains(f['role'], case=False)]
        
        if not res_df.empty:
            # Highlight Top 3
            st.markdown("#### ✨ Premium Matches")
            top_3 = res_df.sort_values(by='salary_max', ascending=False).head(3)
            for _, row in top_3.iterrows():
                flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
                sal = f"{row['salary_min']*f['rate']:,.0f} - {row['salary_max']*f['rate']:,.0f} {f['currency']}" if row['salary_min'] > 0 else "Competitive Market Rate"
                st.markdown(f"""
                    <div class="job-card premium-highlight">
                        <div style="flex:1;">
                            <h2 style="margin:0; font-size:1.6rem; color:#0f172a;">{row['title']} <span style="font-size:11px; color:#6366f1; background:#eef2ff; padding:4px 10px; border-radius:99px; vertical-align:middle;">TOP MATCH</span></h2>
                            <p style="color: #6366f1; font-weight: 700; margin: 10px 0;">{row['company']} • {flag} {row['location']} ({row['country_name']})</p>
                            <p style="color: #64748b; font-size: 0.95rem; font-weight:600;">💰 Benchmark Salary: {sal}</p>
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
                            <h3 style="margin:0; font-size:1.3rem;">{row['title']}</h3>
                            <p style="color: #64748b; font-size: 0.9rem;">{row['company']} • {flag} {row['location']}</p>
                        </div>
                        <a href="{row['url']}" target="_blank" class="apply-btn" style="padding:10px 25px; font-size:0.8rem;">Apply</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No records found for this configuration.")

    # ─── STAGE 3: RESULTS (Analytics) ───
    elif st.session_state.view == "results_analytics":
        f = st.session_state.f
        st.markdown(f"### 📊 Intelligence Report: {', '.join(f['regions'])}")
        if st.button("← Back"): st.session_state.view = "config_analytics"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        sal_clean = res_df[res_df['salary_min'] > 0]
        
        # Plot 1
        st.markdown("#### 💸 Regional Salary Variance")
        fig1 = px.box(sal_clean, x="country_name", y="salary_min", template="plotly_white", color_discrete_sequence=['#6366f1'], labels={"salary_min": f"Salary ({f['currency']})", "country_name": "Region"})
        fig1.update_traces(hovertemplate="<b>%{x}</b><br>Salary: %{y}<extra></extra>")
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('<div class="desc-box">This visualization identifies the pay floor and ceiling across your selected tech hubs. The central box indicates the market median, while dots represent specialized roles that command significant market premiums.</div>', unsafe_allow_html=True)
        
        # Plot 2
        st.markdown("#### 📈 Global Market Share")
        fig2 = px.pie(res_df, names="country_name", hole=0.6, template="plotly_white", color_discrete_sequence=px.colors.sequential.Purples)
        fig2.update_traces(hovertemplate="<b>%{label}</b><br>Share: %{percent}<extra></extra>")
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="desc-box">This chart analyzes job vacancy density. High-percentage regions represent the most active tech economies, suggesting more liquid hiring conditions and a higher probability of successful placement.</div>', unsafe_allow_html=True)

else:
    st.error("Platform engine offline. Check Supabase connection.")
