import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# 1. PAGE CONFIG (Force Sidebar Collapsed)
st.set_page_config(
    page_title="ECHOES | Tech Job Intelligence", 
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

# 3. ELITE GLASSMORPHIC CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .main { background: radial-gradient(circle at top right, #1e1b4b, #020617); }
    
    /* Hiding the sidebar completely via CSS */
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none; }

    /* Landing Hero */
    .hero-title { text-align: center; color: white; font-weight: 800; font-size: 4.5rem; margin-top: 100px; margin-bottom: 10px; }
    .hero-subtitle { text-align: center; color: #818cf8; font-size: 1.3rem; margin-bottom: 60px; font-weight: 400; }
    
    /* Centered Configuration Box */
    .config-box {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 50px;
        border-radius: 30px;
        max-width: 800px;
        margin: 0 auto;
    }

    /* Job Match Cards */
    .job-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 24px; margin-bottom: 25px; }
    .top-match-card { border: 1px solid rgba(99, 102, 241, 0.6) !important; background: rgba(99, 102, 241, 0.08) !important; box-shadow: 0 10px 40px rgba(99, 102, 241, 0.2); }
    
    .desc-text { color: #9ca3af; font-size: 1.1rem; line-height: 1.7; margin-bottom: 50px; padding: 20px; border-left: 4px solid #6366f1; background: rgba(255,255,255,0.02); border-radius: 0 15px 15px 0; }
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
    df['country'] = df['country_code'].map(COUNTRY_MAP).fillna(df['country_code'].str.upper())
    return df

try:
    raw_df = load_data()
except:
    raw_df = pd.DataFrame()

# 5. STATE MANAGEMENT
if 'page' not in st.session_state: st.session_state.page = "landing"
if 'filters' not in st.session_state: st.session_state.filters = {}

def set_page(page_name):
    st.session_state.page = page_name

# 6. APP FLOW
if not raw_df.empty:
    
    # ─── STAGE 1: LANDING PAGE ───
    if st.session_state.page == "landing":
        st.markdown('<h1 class="hero-title">ECHOES 💎</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">The Intelligence Layer for the Global Tech Economy</p>', unsafe_allow_html=True)
        
        c_l, c1, c2, c_r = st.columns([1, 2, 2, 1])
        with c1:
            if st.button("🔍 Launch Job Explorer", use_container_width=True, type="primary"):
                set_page("config_explorer")
                st.rerun()
        with c2:
            if st.button("📊 Launch Market Intelligence", use_container_width=True):
                set_page("config_analytics")
                st.rerun()

    # ─── STAGE 2: CONFIGURATION (Centralized Filtering) ───
    elif st.session_state.page in ["config_explorer", "config_analytics"]:
        st.markdown(f'<h1 style="text-align:center; color:white; margin-top:50px;">Configure Your Insight</h1>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="config-box">', unsafe_allow_html=True)
            
            # Form-like Interface in Main View
            available_countries = sorted(raw_df['country'].unique().tolist())
            col_a, col_b = st.columns(2)
            
            with col_a:
                sel_regions = st.multiselect("Select Regions", available_countries, default=available_countries[:1])
            with col_b:
                sel_currency = st.radio("Display Currency", ["USD", "INR"], horizontal=True)
            
            # Role selection only for Explorer
            sel_role = "All Roles"
            if st.session_state.page == "config_explorer":
                sel_role = st.selectbox("Define Your Target Tech Stack", TECH_ROLES)
            
            st.write("---")
            btn_label = "Generate Market Report" if st.session_state.page == "config_analytics" else "Search Live Market"
            
            c_bl, c_bc, c_br = st.columns([1, 2, 1])
            with c_bc:
                if st.button(btn_label, use_container_width=True, type="primary"):
                    st.session_state.filters = {
                        "regions": sel_regions,
                        "currency": sel_currency,
                        "role": sel_role,
                        "rate": 83.5 if sel_currency == "INR" else 1.0
                    }
                    next_view = "results_explorer" if st.session_state.page == "config_explorer" else "results_analytics"
                    set_page(next_view)
                    st.rerun()
            
            if st.button("← Cancel", use_container_width=False):
                set_page("landing")
                st.rerun()
                
            st.markdown('</div>', unsafe_allow_html=True)

    # ─── STAGE 3: RESULTS (Explorer) ───
    elif st.session_state.page == "results_explorer":
        f = st.session_state.filters
        st.markdown(f"## 🔍 Explorer: {f['role']} in {', '.join(f['regions'])}")
        
        if st.button("🔄 Adjust Filters"): set_page("config_explorer"); st.rerun()
        
        # Filtering logic
        res_df = raw_df[raw_df['country'].isin(f['regions'])]
        if f['role'] != "All Roles":
            res_df = res_df[res_df['title'].str.contains(f['role'], case=False)]
        
        if not res_df.empty:
            # Show Top 3 Recommendations
            st.markdown("### ✨ Premium Matches")
            top_3 = res_df.sort_values(by='salary_max', ascending=False).head(3)
            for _, row in top_3.iterrows():
                sal = f"{row['salary_min']*f['rate']:,.0f} - {row['salary_max']*f['rate']:,.0f} {f['currency']}" if row['salary_min'] > 0 else "Competitive"
                st.markdown(f"""
                    <div class="job-card top-match-card">
                        <a href="{row['url']}" target="_blank" style="float:right; background:#6366f1; color:white; padding:12px 24px; border-radius:14px; font-weight:700; text-decoration:none;">Apply Now</a>
                        <h2 style="margin-top:0;">{row['title']}</h2>
                        <p style="color: #818cf8; font-size:1.1rem; font-weight:600;">{row['company']} • 📍 {row['location']} ({row['country']})</p>
                        <p style="color: #9ca3af; font-size: 0.95rem;">💰 <b>Benchmark Salary:</b> {sal}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            st.markdown(f"### Additional {f['role']} Openings")
            for _, row in res_df.iloc[3:].iterrows():
                st.markdown(f"""
                    <div class="job-card">
                        <a href="{row['url']}" target="_blank" style="float:right; background:rgba(255,255,255,0.08); color:white; padding:10px 20px; border-radius:10px; text-decoration:none;">Apply</a>
                        <h3>{row['title']}</h3>
                        <p style="color: #818cf8;">{row['company']} • 📍 {row['location']} ({row['country']})</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No live records found for this configuration.")

    # ─── STAGE 3: RESULTS (Analytics) ───
    elif st.session_state.page == "results_analytics":
        f = st.session_state.filters
        st.markdown(f"## 📊 Intelligence Report: {', '.join(f['regions'])}")
        if st.button("🔄 Adjust Parameters"): set_page("config_analytics"); st.rerun()

        res_df = raw_df[raw_df['country'].isin(f['regions'])]
        
        # 1. Salary Distribution
        st.markdown("#### 💸 Salary Variance by Region")
        sal_clean = res_df[res_df['salary_min'] > 0]
        if not sal_clean.empty:
            fig1 = px.box(sal_clean, x="country", y="salary_min", color="country", template="plotly_dark", labels={"salary_min": f"Salary ({f['currency']})", "country": "Region"})
            fig1.update_traces(hovertemplate="<b>%{x}</b><br>Salary: %{y}<extra></extra>")
            fig1.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('<div class="desc-text">This visualization maps the pay scales across your selected regions. The central bar represents the market median, while the "whiskers" show the typical salary range for the tech sector in these locations. High outliers often represent lead or staff-level engineering roles.</div>', unsafe_allow_html=True)
        
        # 2. Demand Share
        st.markdown("#### 📈 Global Opportunity Share")
        fig2 = px.pie(res_df, names="country", hole=0.6, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Purples)
        fig2.update_traces(hovertemplate="<b>%{label}</b><br>Share: %{percent}<extra></extra>")
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="desc-text">The "Market Share" donut chart identifies the concentration of active tech vacancies. Use this to determine which geographical hubs are currently experiencing the highest hiring volume, indicating a more robust and liquid job market.</div>', unsafe_allow_html=True)
        
        # 3. Radar
        st.markdown("#### 🎯 Skill Demand Density")
        all_desc = " ".join(res_df['description'].fillna("").tolist()).lower()
        skill_counts = {s: all_desc.count(s.lower()) for s in SKILL_KEYWORDS}
        skill_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Mentions']).sort_values('Mentions', ascending=False)
        fig3 = px.line_polar(skill_df, r='Mentions', theta='Skill', line_close=True, template="plotly_dark")
        fig3.update_traces(fill='toself', line_color='#818cf8', hovertemplate="<b>%{theta}</b><br>Mentions: %{r}<extra></extra>")
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('<div class="desc-text">The radar chart represents the "Technical Pulse" of your selected markets. By analyzing thousands of job descriptions, we calculate the surface area of demand for specific technologies. A shift toward the outer edges signifies a critical requirement for that skill in the current hiring cycle.</div>', unsafe_allow_html=True)

else:
    st.error("Platform is offline. Verify Supabase connection.")
