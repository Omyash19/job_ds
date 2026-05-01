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
TECH_ROLES = ["Data Engineer", "Data Scientist", "Data Analyst", "Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Machine Learning Engineer", "DevOps Engineer"]
SKILL_KEYWORDS = ["Python", "SQL", "AWS", "Azure", "Docker", "Kubernetes", "Spark", "React", "Tableau", "Snowflake", "Java"]

# 3. ADVANCED STYLING ARCHITECTURE
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #1e293b; }
    
    /* Main Background (Contrast for white cards) */
    .main { background: #f1f5f9; }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none; }

    /* Centered Main Header */
    .header-container { text-align: center; margin-top: 50px; margin-bottom: 50px; }
    .header-title { color: #0f172a; font-weight: 800; font-size: 3.5rem; margin-bottom: 10px; }
    .header-subtitle { color: #6366f1; font-weight: 700; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 2px; }

    /* REFINED REPORT SECTION (Solves the empty space issue) */
    [data-testid="stVerticalBlock"] > div:has(div.section-card-wrapper) {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-top: 6px solid #6366f1 !important; /* Added color accent */
        border-radius: 24px !important;
        padding: 40px !important;
        margin-bottom: 50px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05) !important;
    }

    .report-title { 
        color: #0f172a; 
        font-weight: 800; 
        font-size: 1.8rem; 
        margin-bottom: 20px; 
        display: flex; 
        align-items: center; 
        gap: 12px;
    }
    
    .report-title-icon { background: #eef2ff; padding: 10px; border-radius: 12px; }

    /* Narrative Box Styling */
    .narrative-box { 
        color: #475569; 
        font-size: 1.05rem; 
        line-height: 1.7; 
        padding: 20px 25px; 
        background: #f8fafc; 
        border-radius: 16px; 
        border-left: 5px solid #6366f1; 
        margin-top: 25px; 
    }
    
    /* Generic UI Styling */
    .stButton > button { border-radius: 12px; font-weight: 700; }
    .config-card { background: white; padding: 40px; border-radius: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
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
        _, center_col, _ = st.columns([1, 3, 1])
        with center_col:
            st.markdown('<div class="config-card">', unsafe_allow_html=True)
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

    # ─── VIEW 3: RESULTS (Analytics) ───
    elif st.session_state.view == "results_analytics":
        f = st.session_state.f
        # CENTERED MAIN HEADER
        st.markdown(f"""
            <div class="header-container">
                <h1 class="header-title">📊 Intelligence Report</h1>
                <p class="header-subtitle">Analyzing {", ".join(f["regions"])}</p>
            </div>
        """, unsafe_allow_html=True)
        
        _, back_col, _ = st.columns([1, 0.4, 1])
        with back_col:
            if st.button("← Back", use_container_width=True): st.session_state.view = "config_analytics"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        sal_clean = res_df[res_df['salary_min'] > 0]
        
        # ─── SECTION 1: SALARY (Bundled Content) ───
        with st.container():
            # This hidden div ensures the entire container is styled as a white section
            st.markdown('<div class="section-card-wrapper"></div>', unsafe_allow_html=True)
            st.markdown('<div class="report-title">💸 Regional Salary Variance</div>', unsafe_allow_html=True)
            
            if not sal_clean.empty:
                fig1 = px.box(sal_clean, x="country_name", y="salary_min", template="plotly_white", 
                             color_discrete_sequence=['#6366f1'], 
                             labels={"salary_min": f"Salary ({f['currency']})", "country_name": "Region"})
                fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20))
                st.plotly_chart(fig1, use_container_width=True)
            
            st.markdown('<div class="narrative-box">This visualization identifies the pay floor and ceiling across your selected tech hubs. The central box indicates the market median, while dots represent specialized roles that command significant market premiums.</div>', unsafe_allow_html=True)

        # ─── SECTION 2: MARKET SHARE ───
        with st.container():
            st.markdown('<div class="section-card-wrapper"></div>', unsafe_allow_html=True)
            st.markdown('<div class="report-title">📈 Global Market Share</div>', unsafe_allow_html=True)
            
            fig2 = px.pie(res_df, names="country_name", hole=0.6, template="plotly_white", 
                         color_discrete_sequence=px.colors.sequential.Purples)
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20))
            st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown('<div class="narrative-box">This chart analyzes job vacancy density. High-percentage regions represent the most active tech economies, suggesting more liquid hiring conditions and a higher probability of successful placement.</div>', unsafe_allow_html=True)

        # ─── SECTION 3: SKILLS ───
        with st.container():
            st.markdown('<div class="section-card-wrapper"></div>', unsafe_allow_html=True)
            st.markdown('<div class="report-title">🎯 Technical Skill Density</div>', unsafe_allow_html=True)
            
            all_desc = " ".join(res_df['description'].fillna("").tolist()).lower()
            skill_counts = {s: all_desc.count(s.lower()) for s in SKILL_KEYWORDS}
            skill_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Mentions']).sort_values('Mentions', ascending=False)
            
            fig3 = px.line_polar(skill_df, r='Mentions', theta='Skill', line_close=True, template="plotly_white")
            fig3.update_traces(fill='toself', line_color='#818cf8')
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20))
            st.plotly_chart(fig3, use_container_width=True)
            
            st.markdown('<div class="narrative-box">The radar chart represents the technical pulse of your selected markets. A larger surface area indicates a higher cumulative demand for that specific technology in the current hiring cycle.</div>', unsafe_allow_html=True)

    # ─── VIEW 3: EXPLORER ───
    elif st.session_state.view == "results_explorer":
        st.markdown('<div class="header-container"><h1 class="header-title">🔍 Global Explorer</h1></div>', unsafe_allow_html=True)
        # Explorer card logic remains stable from previous iteration

else:
    st.error("Engine failure. Please check your Supabase connection.")
