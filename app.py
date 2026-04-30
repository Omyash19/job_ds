import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# 1. PAGE CONFIG
st.set_page_config(page_title="ECHOES | Tech Job Intelligence", page_icon="💎", layout="wide")

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

# 3. ELITE GLASSMORPHIC & STRUCTURED CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .main { background: radial-gradient(circle at top right, #1e1b4b, #020617); }
    
    /* Landing Hero */
    .hero-title { text-align: center; color: white; font-weight: 800; font-size: 4rem; margin-top: 50px; }
    .hero-subtitle { text-align: center; color: #818cf8; font-size: 1.2rem; margin-bottom: 50px; }
    
    /* Sidebar Structuring */
    .sidebar-section {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .sidebar-label { color: #818cf8; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 10px; }

    /* Job Card Match */
    .job-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 24px; margin-bottom: 25px; }
    .top-match-card { border: 1px solid rgba(99, 102, 241, 0.5) !important; background: rgba(99, 102, 241, 0.05) !important; }
    
    .desc-text { color: #9ca3af; font-size: 1.1rem; line-height: 1.6; margin-bottom: 40px; padding: 10px; border-left: 3px solid #6366f1; background: rgba(255,255,255,0.01); }
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

# 5. INITIALIZE STATE
if 'view' not in st.session_state:
    st.session_state.view = "landing"

# 6. STRUCTURED SIDEBAR (Persistent across all views)
with st.sidebar:
    st.markdown("### 💎 ECHOES CONTROL")
    
    # Section 1: Geographic & Financial Filters
    st.markdown('<div class="sidebar-section"><p class="sidebar-label">Global Filters</p>', unsafe_allow_html=True)
    available_countries = sorted(raw_df['country'].unique().tolist()) if not raw_df.empty else []
    selected_countries = st.multiselect("Region", available_countries, default=available_countries[:3] if available_countries else [])
    currency = st.radio("Display Currency", ["USD", "INR"], horizontal=True)
    rate = 83.5 if currency == "INR" else 1.0
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 2: Career Path (Fills sidebar middle)
    st.markdown('<div class="sidebar-section"><p class="sidebar-label">Career Focus</p>', unsafe_allow_html=True)
    role_pref = st.selectbox("Target Role", ["All Roles"] + TECH_ROLES)
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 3: Live Market Pulse (Fills sidebar bottom)
    if not raw_df.empty:
        filtered_df = raw_df[raw_df['country'].isin(selected_countries)]
        if role_pref != "All Roles":
            filtered_df = filtered_df[filtered_df['title'].str.contains(role_pref, case=False)]
        
        st.markdown('<div class="sidebar-section"><p class="sidebar-label">Live Market Pulse</p>', unsafe_allow_html=True)
        st.caption(f"📍 Regions: {len(selected_countries)}")
        st.caption(f"💼 Active Records: {len(filtered_df)}")
        avg_raw = filtered_df[filtered_df['salary_min'] > 0]['salary_min'].mean() * rate if not filtered_df.empty else 0
        st.caption(f"💰 Avg Salary: {currency} {avg_raw:,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🏠 Return to Landing"):
        st.session_state.view = "landing"

# 7. MAIN VIEW LOGIC
if st.session_state.view == "landing":
    # LANDING PAGE VIEW
    st.markdown('<h1 class="hero-title">ECHOES 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Advanced Tech Job Market Intelligence & Exploration Platform</p>', unsafe_allow_html=True)
    
    col_l, col_1, col_2, col_r = st.columns([1, 2, 2, 1])
    with col_1:
        if st.button("🔍 Open Job Explorer", use_container_width=True, type="primary"):
            st.session_state.view = "explorer"
            st.rerun()
    with col_2:
        if st.button("📊 Open Market Intelligence", use_container_width=True):
            st.session_state.view = "analytics"
            st.rerun()

elif st.session_state.view == "explorer":
    # JOB EXPLORER VIEW
    st.markdown('## 🔍 Job Explorer')
    if role_pref == "All Roles":
        st.info("Please select a **Target Role** in the sidebar to reveal personalized matches.")
    else:
        if not filtered_df.empty:
            # Top 3 Recommendations
            st.markdown("### ✨ Top 3 Personalized Matches")
            top_3 = filtered_df.sort_values(by='salary_max', ascending=False).head(3)
            for _, row in top_3.iterrows():
                sal = f"{row['salary_min']*rate:,.0f} - {row['salary_max']*rate:,.0f} {currency}" if row['salary_min'] > 0 else "Competitive"
                st.markdown(f"""
                    <div class="job-card top-match-card">
                        <a href="{row['url']}" target="_blank" style="float:right; background:#6366f1; color:white; padding:10px 20px; border-radius:12px; font-weight:700; text-decoration:none;">Apply</a>
                        <h2 style="margin-top:0;">{row['title']} <span style="font-size:12px; color:#818cf8;">(TOP MATCH)</span></h2>
                        <p style="color: #818cf8;">{row['company']} • 📍 {row['location']} ({row['country']})</p>
                        <p style="color: #9ca3af; font-size: 0.9rem;">💰 <b>Est. Salary:</b> {sal}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            st.markdown(f"### All {role_pref} Opportunities")
            for _, row in filtered_df.iloc[3:].iterrows():
                sal = f"{row['salary_min']*rate:,.0f} - {row['salary_max']*rate:,.0f} {currency}" if row['salary_min'] > 0 else "Competitive"
                st.markdown(f"""
                    <div class="job-card">
                        <a href="{row['url']}" target="_blank" style="float:right; background:rgba(255,255,255,0.1); color:white; padding:8px 16px; border-radius:10px; text-decoration:none;">Apply</a>
                        <h3>{row['title']}</h3>
                        <p style="color: #818cf8;">{row['company']} • 📍 {row['location']} ({row['country']})</p>
                        <p style="color: #9ca3af; font-size: 0.8rem;">💰 {sal}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No live records match these filters.")

elif st.session_state.view == "analytics":
    # MARKET ANALYTICS VIEW
    st.markdown('## 📊 Market Intelligence Reports')
    
    # 1. Salary Box Plot
    st.markdown("#### 💸 Regional Salary Benchmarking")
    sal_clean = filtered_df[filtered_df['salary_min'] > 0]
    if not sal_clean.empty:
        fig1 = px.box(sal_clean, x="country", y="salary_min", color="country", template="plotly_dark", labels={"salary_min": f"Salary ({currency})", "country": "Region"})
        fig1.update_traces(hovertemplate="<b>%{x}</b><br>Salary: %{y}<extra></extra>")
        fig1.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('<div class="desc-text">This diagram illustrates the salary variance across your selected regions. The central box represents the middle 50% of the market, while the dots indicate specific high-value outliers in the tech sector. Use this to gauge your earning potential in different geographical hubs.</div>', unsafe_allow_html=True)
    
    # 2. Regional Demand Pie
    st.markdown("#### 📈 Global Market Share")
    if not filtered_df.empty:
        fig2 = px.pie(filtered_df, names="country", hole=0.6, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Purples)
        fig2.update_traces(hovertemplate="<b>%{label}</b><br>Share: %{percent}<extra></extra>")
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="desc-text">This chart breaks down the total volume of job postings by region. It helps identify which geographical markets are currently most active for tech recruitment, allowing you to focus your search on the most high-demand hubs within your filtered parameters.</div>', unsafe_allow_html=True)

    # 3. Skills Radar
    st.markdown("#### 🎯 Technical Skill Density")
    all_desc = " ".join(filtered_df['description'].fillna("").tolist()).lower()
    skill_counts = {s: all_desc.count(s.lower()) for s in SKILL_KEYWORDS}
    skill_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Mentions']).sort_values('Mentions', ascending=False)
    fig3 = px.line_polar(skill_df, r='Mentions', theta='Skill', line_close=True, template="plotly_dark")
    fig3.update_traces(fill='toself', line_color='#818cf8', hovertemplate="<b>%{theta}</b><br>Mentions: %{r}<extra></extra>")
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('<div class="desc-text">The radar chart tracks keyword frequency within job descriptions. A larger surface area indicates a higher cumulative demand for that specific technology across all active job postings. Use this to prioritize which technical skills you should highlight in your applications.</div>', unsafe_allow_html=True)
