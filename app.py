import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go

# 1. MASTER CONFIG
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
COUNTRY_FLAGS = {"us": "🇺🇸", "gb": "🇬🇧", "in": "🇮🇳", "au": "🇦🇺", "ca": "🇨🇦", "de": "🇩🇪", "fr": "🇫🇷"}
TECH_ROLES = ["Data Engineer", "Data Scientist", "Data Analyst", "Software Engineer", "Machine Learning Engineer", "DevOps Engineer"]
SKILL_KEYWORDS = ["Python", "SQL", "AWS", "Azure", "Docker", "Kubernetes", "Spark", "React", "Tableau", "Snowflake", "Java"]

# 3. UNIFIED ONE-PAGE CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    html, body, [class*="css"], [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #1e293b; }
    
    .stApp {
        background: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.1) 0px, transparent 50%),
                    radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.1) 0px, transparent 50%),
                    #F8FAFC;
    }

    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }

    /* Centered Branding */
    .master-header { text-align: center; margin-top: 40px; margin-bottom: 40px; }
    .master-title { color: #0f172a; font-weight: 800; font-size: 3.5rem; margin-bottom: 0px; letter-spacing: -1.5px; }
    .master-subtitle { color: #6366f1; font-weight: 700; font-size: 1rem; text-transform: uppercase; letter-spacing: 2.5px; }

    /* One-Page Filter Card */
    .filter-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid white;
        padding: 35px;
        border-radius: 24px;
        box-shadow: 0 20px 40px -10px rgba(0,0,0,0.05);
        margin-bottom: 60px;
    }

    /* Horizontal Job Card */
    .job-card {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 25px 35px;
        border-radius: 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease;
    }
    .job-card:hover { transform: translateX(8px); border-left: 6px solid #6366f1; box-shadow: 15px 15px 35px rgba(0,0,0,0.04); }
    
    .apply-link {
        background: #6366f1;
        color: white !important;
        padding: 10px 24px;
        border-radius: 12px;
        text-decoration: none !important;
        font-weight: 700;
        font-size: 0.9rem;
    }

    /* Report Section Card */
    .report-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-top: 6px solid #6366f1;
        padding: 40px;
        border-radius: 24px;
        margin-bottom: 40px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03);
    }
    .report-title { color: #0f172a; font-weight: 800; font-size: 1.8rem; margin-bottom: 25px; }
    
    .narrative-box { 
        color: #475569; font-size: 1rem; line-height: 1.7; padding: 20px; 
        background: #f8fafc; border-radius: 15px; border-left: 4px solid #6366f1; margin-top: 25px; 
    }

    .stButton > button { border-radius: 12px; font-weight: 700; height: 3.5em; width: 100%; transition: all 0.2s; }
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

# 5. INITIAL STATE
if 'triggered' not in st.session_state: st.session_state.triggered = False

# 6. APP CONTENT (ONE PAGE FLOW)
st.markdown('<div class="master-header"><h1 class="master-title">ECHOES 💎</h1><p class="master-subtitle">Intelligence for the Tech Economy</p></div>', unsafe_allow_html=True)

if not raw_df.empty:
    # ─── MASTER FILTER SECTION ───
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1.5])
    with c1:
        sel_regions = st.multiselect("Select Target Regions", sorted(raw_df['country_name'].unique().tolist()), default=[raw_df['country_name'].unique().tolist()[0]])
    with c2:
        sel_currency = st.radio("Currency", ["USD", "INR"], horizontal=True)
        rate = 83.5 if sel_currency == "INR" else 1.0
    with c3:
        sel_role = st.selectbox("Tech Stack Preference", ["All Tech Roles"] + TECH_ROLES)
    
    st.write("---")
    if st.button("✨ GENERATE MARKET INTELLIGENCE", type="primary"):
        st.session_state.triggered = True
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── RESULTS SECTION (Only shows after trigger) ───
    if st.session_state.triggered:
        # Data Filtering
        res_df = raw_df[raw_df['country_name'].isin(sel_regions)]
        if sel_role != "All Tech Roles":
            res_df = res_df[res_df['title'].str.contains(sel_role, case=False)]

        # TABBED INTERFACE FOR ONE-PAGE DENSITY
        tab1, tab2 = st.tabs(["📊 Market Analysis (3 Reports)", "🔍 Live Job Explorer"])

        with tab1:
            st.markdown("<br/>", unsafe_allow_html=True)
            sal_clean = res_df[res_df['salary_min'] > 0]
            
            # --- REPORT 1: SALARY ---
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.markdown('<div class="report-title">💸 01. Regional Salary Variance</div>', unsafe_allow_html=True)
            if not sal_clean.empty:
                fig1 = px.box(sal_clean, x="country_name", y="salary_min", template="plotly_white", color_discrete_sequence=['#6366f1'])
                fig1.update_traces(hovertemplate="<b>%{x}</b><br>Benchmarked: " + sel_currency + " %{y:,.0f}")
                fig1.update_layout(margin=dict(t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
            st.markdown('<div class="narrative-box">Identification of regional pay floors and ceilings. Outliers indicate specialized senior roles commanding significant premiums in these hubs.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # --- REPORT 2: MARKET SHARE ---
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.markdown('<div class="report-title">📈 02. Global Hub Market Share</div>', unsafe_allow_html=True)
            fig2 = px.pie(res_df, names="country_name", hole=0.5, template="plotly_white", color_discrete_sequence=px.colors.sequential.Purples_r)
            fig2.update_layout(margin=dict(t=0, b=0), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('<div class="narrative-box">Analysis of job vacancy density. Larger slices represent the most active tech economies, suggesting higher liquidity for job seekers.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # --- REPORT 3: SKILL PULSE ---
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.markdown('<div class="report-title">🎯 03. Technical Skill Demand Pulse</div>', unsafe_allow_html=True)
            all_desc = " ".join(res_df['description'].fillna("").tolist()).lower()
            skill_counts = {s: all_desc.count(s.lower()) for s in SKILL_KEYWORDS}
            skill_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Mentions']).sort_values('Mentions', ascending=False)
            
            fig3 = px.line_polar(skill_df, r='Mentions', theta='Skill', line_close=True, template="plotly_white")
            fig3.update_traces(fill='toself', fillcolor='rgba(99, 102, 241, 0.3)', line_color='#6366f1')
            fig3.update_layout(margin=dict(t=30, b=30), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('<div class="narrative-box">The radar chart maps the surface area of demand for specific skillsets. A wider pull toward the edges signifies critical hiring requirements.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown("<br/>", unsafe_allow_html=True)
            if not res_df.empty:
                for _, row in res_df.iterrows():
                    flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
                    sal = f"{row['salary_min']*rate:,.0f} - {row['salary_max']*rate:,.0f} {sel_currency}" if row['salary_min'] > 0 else "Benchmark Disclosed on Apply"
                    st.markdown(f"""
                        <div class="job-card">
                            <div style="flex:1;">
                                <h3 style="margin:0; font-size:1.4rem; color:#0f172a;">{row['title']}</h3>
                                <p style="color: #6366f1; font-weight: 700; margin: 8px 0;">{row['company']} • {flag} {row['location']} ({row['country_name']})</p>
                                <p style="color: #64748b; font-size: 0.9rem; font-weight:600;">Benchmark: {sal}</p>
                            </div>
                            <a href="{row['url']}" target="_blank" class="apply-link">Apply Now</a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No matching live records found for this configuration.")

else:
    st.error("Platform engine offline. Please verify database connectivity.")
