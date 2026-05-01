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

# 3. ADVANCED MODULAR CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #1e293b; }
    
    /* Background & Sidebar Hide */
    .main { background: #f8fafc; }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none; }

    /* Hero Branding */
    .hero-title { text-align: center; color: #0f172a; font-weight: 800; font-size: 3.8rem; margin-top: 50px; }
    .hero-subtitle { text-align: center; color: #6366f1; font-size: 1.1rem; margin-bottom: 40px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Center Aligned Analytics Header */
    .report-main-header { text-align: center; color: #0f172a; font-weight: 800; font-size: 3rem; margin-top: 40px; margin-bottom: 10px; }
    .report-sub-header { text-align: center; color: #64748b; font-size: 1.2rem; margin-bottom: 50px; }

    /* Glassmorphic Report Block (Outline) */
    .report-block {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(226, 232, 240, 0.8);
        padding: 40px;
        border-radius: 32px;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
    }
    .report-block-title { color: #0f172a; font-weight: 800; font-size: 1.8rem; margin-bottom: 25px; display: flex; align-items: center; gap: 10px; }

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

    /* Horizontal Glass Job Card */
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
    }
    
    .apply-btn {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white !important;
        padding: 12px 30px;
        border-radius: 16px;
        text-decoration: none;
        font-weight: 700;
        font-size: 14px;
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
    }

    /* Narrative Design */
    .desc-box { color: #475569; font-size: 1.05rem; line-height: 1.7; padding: 20px 25px; background: rgba(99, 102, 241, 0.03); border-radius: 16px; border-left: 4px solid #6366f1; margin-top: 20px; }
    
    .stButton > button { border-radius: 14px; font-weight: 700; }
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
        st.markdown('<h1 class="hero-title">ECHOES 💎</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">The Intelligence Layer for the Tech Economy</p>', unsafe_allow_html=True)
        
        _, col1, col2, _ = st.columns([1, 2.2, 2.2, 1])
        with col1:
            if st.button("🔍 Launch Job Explorer", use_container_width=True, type="primary"):
                st.session_state.view = "config_explorer"; st.rerun()
        with col2:
            if st.button("📊 Market Intelligence", use_container_width=True):
                st.session_state.view = "config_analytics"; st.rerun()

    # ─── VIEW 2: CONFIGURATION ───
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
            btn_label = "Search Live Market" if st.session_state.view == "config_explorer" else "Generate Intelligence"
            if st.button(btn_label, use_container_width=True, type="primary"):
                st.session_state.f = {"regions": sel_regions, "currency": sel_currency, "role": sel_role, "rate": 83.5 if sel_currency == "INR" else 1.0}
                st.session_state.view = "results_explorer" if st.session_state.view == "config_explorer" else "results_analytics"
                st.rerun()
            if st.button("← Back", use_container_width=True):
                st.session_state.view = "landing"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ─── VIEW 3: RESULTS (Explorer) ───
    elif st.session_state.view == "results_explorer":
        f = st.session_state.f
        st.markdown(f'<h1 class="report-main-header">🔍 Global Explorer</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="report-sub-header">{f["role"]} roles across {", ".join(f["regions"])}</p>', unsafe_allow_html=True)
        
        c_l, c_btn, c_r = st.columns([1, 0.5, 1])
        with c_btn:
            if st.button("← Back"): st.session_state.view = "config_explorer"; st.rerun()

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
                            <p style="color: #6366f1; font-weight: 700; margin: 10px 0;">{row['company']} • {flag} {row['location']} ({row['country_name']})</p>
                            <p style="color: #64748b; font-size: 0.95rem; font-weight:600;">💰 Benchmark Salary: {sal}</p>
                        </div>
                        <a href="{row['url']}" target="_blank" class="apply-btn">Apply Now</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No records found for this configuration.")

    # ─── VIEW 3: RESULTS (Analytics) ───
    elif st.session_state.view == "results_analytics":
        f = st.session_state.f
        # Centered Big Header
        st.markdown(f'<h1 class="report-main-header">📊 Intelligence Report</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="report-sub-header">Analyzing trends for {", ".join(f["regions"])}</p>', unsafe_allow_html=True)
        
        c_l, c_btn, c_r = st.columns([1, 0.5, 1])
        with c_btn:
            if st.button("← Back"): st.session_state.view = "config_analytics"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        sal_clean = res_df[res_df['salary_min'] > 0]
        
        # Report Section 1: Salary
        st.markdown('<div class="report-block">', unsafe_allow_html=True)
        st.markdown('<div class="report-block-title">💸 Regional Salary Variance</div>', unsafe_allow_html=True)
        if not sal_clean.empty:
            fig1 = px.box(sal_clean, x="country_name", y="salary_min", template="plotly_white", color_discrete_sequence=['#6366f1'], labels={"salary_min": f"Salary ({f['currency']})", "country_name": "Region"})
            fig1.update_traces(hovertemplate="<b>%{x}</b><br>Salary: %{y}<extra></extra>")
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('<div class="desc-box">This visualization identifies the pay floor and ceiling across your selected tech hubs. The central box indicates the market median, while dots represent specialized roles that command significant market premiums.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Report Section 2: Market Share
        st.markdown('<div class="report-block">', unsafe_allow_html=True)
        st.markdown('<div class="report-block-title">📈 Global Market Share</div>', unsafe_allow_html=True)
        fig2 = px.pie(res_df, names="country_name", hole=0.6, template="plotly_white", color_discrete_sequence=px.colors.sequential.Purples)
        fig2.update_traces(hovertemplate="<b>%{label}</b><br>Share: %{percent}<extra></extra>")
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="desc-box">This chart analyzes job vacancy density. High-percentage regions represent the most active tech economies, suggesting more liquid hiring conditions and a higher probability of successful placement.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Report Section 3: Skill Demand
        st.markdown('<div class="report-block">', unsafe_allow_html=True)
        st.markdown('<div class="report-block-title">🎯 Technical Skill Density</div>', unsafe_allow_html=True)
        all_desc = " ".join(res_df['description'].fillna("").tolist()).lower()
        skill_counts = {s: all_desc.count(s.lower()) for s in SKILL_KEYWORDS}
        skill_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Mentions']).sort_values('Mentions', ascending=False)
        fig3 = px.line_polar(skill_df, r='Mentions', theta='Skill', line_close=True, template="plotly_white")
        fig3.update_traces(fill='toself', line_color='#818cf8', hovertemplate="<b>%{theta}</b><br>Mentions: %{r}<extra></extra>")
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('<div class="desc-box">The radar chart represents the technical pulse of your selected markets. A larger surface area indicates a higher cumulative demand for that specific technology in the current hiring cycle.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error("Platform engine offline. Check Supabase connection.")
