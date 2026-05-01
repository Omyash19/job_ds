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

# 3. ADVANCED GLASSMORPHIC UI (Bright Mode)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #1e293b; }
    
    .main { background: #f1f5f9; }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none; }

    /* Centered Header */
    .header-container { text-align: center; margin-top: 40px; margin-bottom: 50px; width: 100%; }
    .header-title { color: #0f172a; font-weight: 800; font-size: 3.8rem; margin-bottom: 0px; }
    .header-subtitle { color: #6366f1; font-weight: 700; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 2px; }

    /* Modular Report Sections */
    .report-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-top: 6px solid #6366f1;
        padding: 45px;
        border-radius: 28px;
        margin-bottom: 50px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }
    
    .report-title { 
        color: #0f172a; 
        font-weight: 800; 
        font-size: 2rem; 
        margin-bottom: 30px; 
        display: flex; 
        align-items: center; 
        gap: 15px;
    }

    .narrative-box { 
        color: #475569; 
        font-size: 1.1rem; 
        line-height: 1.8; 
        padding: 25px; 
        background: #f8fafc; 
        border-radius: 18px; 
        border-left: 6px solid #6366f1; 
        margin-top: 30px; 
    }

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
        st.markdown('<div class="header-container"><h1 class="header-title">ECHOES 💎</h1><p class="header-subtitle">The Intelligence Layer for the Tech Economy</p></div>', unsafe_allow_html=True)
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

    # ─── VIEW 3: ANALYTICS (Sharpened Visuals) ───
    elif st.session_state.view == "results_analytics":
        f = st.session_state.f
        
        # CENTERED MAIN HEADER
        st.markdown(f"""
            <div class="header-container">
                <h1 class="header-title">📊 Intelligence Report</h1>
                <p class="header-subtitle">Analyzing Trends for {", ".join(f["regions"])}</p>
            </div>
        """, unsafe_allow_html=True)
        
        _, back_col, _ = st.columns([1, 0.4, 1])
        with back_col:
            if st.button("← Back", use_container_width=True): 
                st.session_state.view = "config_analytics"
                st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        sal_clean = res_df[res_df['salary_min'] > 0]
        
        # Professional Chart Configuration
        chart_theme = dict(
            font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#475569"),
            margin=dict(t=40, b=40, l=40, r=40),
            hoverlabel=dict(bgcolor="white", font_size=13, font_family="Plus Jakarta Sans")
        )

        # ─── SECTION 1: SALARY (High Contrast & Formatted) ───
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.markdown('<div class="report-title">💸 Regional Salary Variance</div>', unsafe_allow_html=True)
        
        if not sal_clean.empty:
            fig1 = px.box(
                sal_clean, 
                x="country_name", 
                y="salary_min", 
                template="plotly_white", 
                color="country_name",
                color_discrete_sequence=["#6366f1", "#8b5cf6", "#3b82f6"],
                labels={"salary_min": f"Annual Salary ({f['currency']})", "country_name": "Market"}
            )
            # Precision tooltips: Rounded to 1 decimal with currency suffix
            fig1.update_traces(
                marker_color="#6366f1",
                line_width=2,
                hovertemplate="<b>%{x}</b><br>Benchmarked: " + f"{f['currency']} " + "%{y:,.1f}<extra></extra>"
            )
            fig1.update_layout(**chart_theme, showlegend=False, yaxis=dict(gridcolor="#f1f5f9"))
            st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown('<div class="narrative-box">This visualization identifies the pay floor and ceiling across your selected tech hubs. The central box indicates the market median, while dots represent specialized roles that command significant market premiums.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ─── SECTION 2: MARKET SHARE (Vibrant Palette) ───
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.markdown('<div class="report-title">📈 Global Market Share</div>', unsafe_allow_html=True)
        
        fig2 = px.pie(
            res_df, 
            names="country_name", 
            hole=0.5, 
            template="plotly_white", 
            color_discrete_sequence=["#6366f1", "#a5b4fc", "#e0e7ff", "#312e81"]
        )
        fig2.update_traces(
            textposition='outside', 
            textinfo='percent+label',
            marker=dict(line=dict(color='white', width=3)),
            hovertemplate="<b>%{label}</b><br>Market Share: %{percent}<extra></extra>"
        )
        fig2.update_layout(**chart_theme, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown('<div class="narrative-box">This chart analyzes job vacancy density. High-percentage regions represent the most active tech economies, suggesting more liquid hiring conditions and a higher probability of successful placement.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ─── SECTION 3: SKILLS (Bold Interactivity) ───
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.markdown('<div class="report-title">🎯 Technical Skill Density</div>', unsafe_allow_html=True)
        
        all_desc = " ".join(res_df['description'].fillna("").tolist()).lower()
        skill_counts = {s: all_desc.count(s.lower()) for s in SKILL_KEYWORDS}
        skill_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Mentions']).sort_values('Mentions', ascending=False)
        
        fig3 = px.line_polar(
            skill_df, 
            r='Mentions', 
            theta='Skill', 
            line_close=True, 
            template="plotly_white"
        )
        # Bold borders and higher fill opacity for readability
        fig3.update_traces(
            fill='toself', 
            fillcolor='rgba(99, 102, 241, 0.4)',
            line_color='#6366f1', 
            line_width=3,
            hovertemplate="<b>%{theta}</b><br>Demand Index: %{r}<extra></extra>"
        )
        fig3.update_layout(**chart_theme, polar=dict(radialaxis=dict(visible=True, gridcolor="#f1f5f9"), angularaxis=dict(gridcolor="#f1f5f9")))
        st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown('<div class="narrative-box">The radar chart represents the technical pulse of your selected markets. A larger surface area indicates a higher cumulative demand for that specific technology in the current hiring cycle.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── VIEW 3: EXPLORER ───
    elif st.session_state.view == "results_explorer":
        st.markdown('<div class="header-container"><h1 class="header-title">🔍 Global Explorer</h1></div>', unsafe_allow_html=True)
        # (Existing Explorer card logic follows...)

else:
    st.error("Platform engine offline. Check Supabase connection.")
