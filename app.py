import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# 1. PAGE CONFIG
st.set_page_config(
    page_title="ECHOES | Global Tech Intelligence", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state=import streamlit as st
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

# 3. ADVANCED UI FINISHING (CSS) - Glassmorphism (Bright Mode)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"], [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #0f172a; }
    
    /* Solid Background */
    .stApp { background: #F8FAFC; }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; } /* Hide the sidebar expand control entirely */

    /* Titles & Headings */
    .hero-title { text-align: center; color: #0f172a; font-weight: 800; font-size: 4rem; margin-top: 50px; margin-bottom: 5px; }
    .hero-subtitle { text-align: center; color: #6366f1; font-size: 1.1rem; margin-bottom: 40px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; }
    .section-header { text-align: center; color: #0f172a; font-weight: 800; font-size: 2.2rem; margin-bottom: 20px; }

    /* Glassmorphism Inputs */
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"], div[data-testid="stRadio"] > div {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(20px);
        border: 1px solid white !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Fix for multi-select tags */
    span[data-baseweb="tag"] {
        background: #6366f1 !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* Horizontal Glass Job Card */
    .job-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 25px 35px;
        border-radius: 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid white;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        text-decoration: none !important;
    }
    .job-card:hover { 
        transform: translateY(-4px); 
        box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.1); 
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    .premium-card {
        border: 2px solid #6366f1;
    }
    
    .apply-btn {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white !important;
        padding: 12px 30px;
        border-radius: 14px;
        text-decoration: none !important;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
        white-space: nowrap;
        border: none;
    }
    .apply-btn:hover {
        opacity: 0.9;
    }
    
    /* Data Storytelling */
    .desc-box { 
        color: #475569; 
        font-size: 1rem; 
        line-height: 1.7; 
        padding-left: 20px;
        margin-top: 15px;
        margin-left: 20px;
        margin-bottom: 40px; 
        border-left: 3px solid #6366f1; 
    }
    
    /* Standardizing Button Styles */
    .stButton > button { 
        border-radius: 12px; 
        font-weight: 700; 
        height: 3em; 
        border: 1px solid white;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        color: #0f172a;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        border-color: #6366f1;
        color: #6366f1;
    }
    
    /* Primary buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
    }
    
    /* Glassmorphism Configuration Card via marker hack */
    [data-testid="column"] > div[data-testid="stVerticalBlock"]:has(.config-card-marker) {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid white;
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05);
        max-width: 850px;
        margin: 0 auto;
    }
    
    /* Remove grey block artifacts */
    .element-container:empty { display: none; }
    
    /* Remove redundant link icons */
    .stMarkdown a svg { display: none !important; }
    </style>
""", unsafe_allow_html=True)

import random

# 4. DATA ENGINE (Dummy Data for UI Preview)
@st.cache_data
def load_data():
    # Generating dummy job records to showcase the UI perfectly
    companies = ["Google", "Meta", "Stripe", "Airbnb", "Netflix", "Spotify", "Uber", "Databricks", "Snowflake", "OpenAI"]
    locations = ["Remote", "New York", "San Francisco", "London", "Berlin", "Toronto", "Sydney", "Bangalore"]
    countries = ["us", "us", "us", "gb", "de", "ca", "au", "in"]
    
    data = []
    for _ in range(50):
        role = random.choice(TECH_ROLES)
        company = random.choice(companies)
        idx = random.randint(0, len(locations)-1)
        loc = locations[idx]
        country = countries[idx]
        
        base_salary = random.randint(70000, 180000)
        
        data.append({
            "title": f"Senior {role}" if random.random() > 0.5 else role,
            "company": company,
            "country": country,
            "location": loc,
            "salary_min": base_salary,
            "salary_max": base_salary + random.randint(20000, 50000),
            "url": "#"
        })
        
    df = pd.DataFrame(data)
    df['country_code'] = df['country'].str.lower()
    df['country_name'] = df['country_code'].map(COUNTRY_MAP).fillna(df['country_code'].str.upper())
    return df

raw_df = load_data()

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
            if st.button("📊 Market Intelligence", use_container_width=True, type="primary"):
                st.session_state.page = "config_analytics"; st.rerun()

    # ─── VIEW 2: CONFIGURATION PAGE ───
    elif st.session_state.page in ["config_explorer", "config_analytics"]:
        st.markdown('<h2 class="section-header">Configure Your Insight</h2>', unsafe_allow_html=True)
        
        # Center aligning using columns
        _, center_col, _ = st.columns([1, 2.5, 1])
        
        with center_col:
            st.markdown("<div class='config-card-marker'></div>", unsafe_allow_html=True)
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
            
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True) # Spacing
            
            # Action Buttons
            btn_label = "Search Live Market" if st.session_state.page == "config_explorer" else "Generate Market Report"
            if st.button(btn_label, use_container_width=True, type="primary"):
                st.session_state.filters = {"regions": sel_regions, "currency": sel_currency, "role": sel_role, "rate": 83.5 if sel_currency == "INR" else 1.0}
                st.session_state.page = "results_explorer" if st.session_state.page == "config_explorer" else "results_analytics"
                st.rerun()
            
            # Back Button
            if st.button("← Back", use_container_width=True):
                st.session_state.page = "landing"; st.rerun()

    # ─── VIEW 3: RESULTS (Explorer) ───
    elif st.session_state.page == "results_explorer":
        f = st.session_state.filters
        st.markdown(f'<h3 style="color:#0f172a;">🔍 Explorer: {f["role"]} in {", ".join(f["regions"])}</h3>', unsafe_allow_html=True)
        if st.button("← Back"): st.session_state.page = "config_explorer"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        if f['role'] != "All Roles":
            res_df = res_df[res_df['title'].str.contains(f['role'], case=False)]
        
        if not res_df.empty:
            st.markdown('<h4 style="color:#0f172a; margin-top:20px;">✨ Premium Matches</h4>', unsafe_allow_html=True)
            top_3 = res_df.sort_values(by='salary_max', ascending=False).head(3)
            for _, row in top_3.iterrows():
                flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
                sal = f"{row['salary_min']*f['rate']:,.0f} - {row['salary_max']*f['rate']:,.0f} {f['currency']}" if row['salary_min'] > 0 else "Competitive Market Rate"
                st.markdown(f"""
                    <div class="job-card premium-card">
                        <div style="flex:1; text-align: left;">
                            <h2 style="margin:0; font-size:1.5rem; color:#0f172a;">{row['title']}</h2>
                            <p style="color: #6366f1; font-weight: 700; margin: 8px 0; font-size:1rem;">{row['company']} • {flag} {row['location']} ({row['country_name']})</p>
                            <p style="color: #475569; font-size: 0.9rem; font-weight:600; margin:0;">Benchmark: {sal}</p>
                        </div>
                        <a href="{row['url']}" target="_blank" class="apply-btn">Apply Now</a>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br/>", unsafe_allow_html=True)
            for _, row in res_df.iloc[3:].iterrows():
                flag = COUNTRY_FLAGS.get(row['country_code'], "📍")
                sal = f"{row['salary_min']*f['rate']:,.0f} - {row['salary_max']*f['rate']:,.0f} {f['currency']}" if row['salary_min'] > 0 else "Competitive Market Rate"
                st.markdown(f"""
                    <div class="job-card">
                        <div style="flex:1; text-align: left;">
                            <h3 style="margin:0; font-size:1.2rem; color:#0f172a;">{row['title']}</h3>
                            <p style="color: #6366f1; font-size: 0.9rem; margin: 8px 0;">{row['company']} • {flag} {row['location']} ({row['country_name']})</p>
                            <p style="color: #475569; font-size: 0.8rem; font-weight:600; margin:0;">Benchmark: {sal}</p>
                        </div>
                        <a href="{row['url']}" target="_blank" class="apply-btn" style="padding:10px 25px; font-size:0.8rem;">Apply Now</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No records found for this market segment.")

    # ─── VIEW 3: RESULTS (Analytics) ───
    elif st.session_state.page == "results_analytics":
        f = st.session_state.filters
        st.markdown(f'<h3 style="color:#0f172a;">📊 Intelligence Report: {", ".join(f["regions"])}</h3>', unsafe_allow_html=True)
        if st.button("← Back"): st.session_state.page = "config_analytics"; st.rerun()

        res_df = raw_df[raw_df['country_name'].isin(f['regions'])]
        
        k1, k2, k3 = st.columns(3)
        sal_clean = res_df[res_df['salary_min'] > 0]
        avg = (sal_clean['salary_min'].mean() + sal_clean['salary_max'].mean()) / 2 * f['rate'] if not sal_clean.empty else 0
        k1.metric("Live Sample Size", f"{len(res_df)} Roles")
        k2.metric(f"Market Midpoint ({f['currency']})", f"{avg:,.0f}" if avg > 0 else "N/A")
        k3.metric("Top Hiring Hub", res_df['country_name'].value_counts().idxmax() if not res_df.empty else "N/A")

        st.markdown('<h4 style="color:#0f172a; margin-top:30px;">💸 Salary Benchmarking</h4>', unsafe_allow_html=True)
        fig1 = px.box(sal_clean, x="country_name", y="salary_min", 
                      template="plotly_white", 
                      color_discrete_sequence=['#6366f1'],
                      hover_data={"country_name": True})
        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Plus Jakarta Sans", color="#0f172a")
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('<div class="desc-box">Comparative analysis of regional pay scales. Outliers indicate specialized roles with higher market premiums.</div>', unsafe_allow_html=True)

else:
    st.error("Engine failure. Please check your connection.")"collapsed"
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
