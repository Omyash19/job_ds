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

# 3. ELITE GLASSMORPHIC CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .main { background: radial-gradient(circle at top right, #1e1b4b, #020617); }
    
    /* Center Title */
    .center-title { text-align: center; color: white; font-weight: 800; font-size: 3rem; margin-bottom: 0px; }
    
    /* KPI Card */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 20px;
    }
    
    /* Job Card */
    .job-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 24px;
        margin-bottom: 25px;
    }
    .top-match-card {
        border: 1px solid rgba(99, 102, 241, 0.5) !important;
        background: rgba(99, 102, 241, 0.05) !important;
    }
    .skill-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.1);
        color: #818cf8;
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 11px;
        margin-right: 8px;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    .desc-text { color: #9ca3af; font-size: 1.1rem; line-height: 1.6; margin-bottom: 40px; }
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
except Exception as e:
    st.error(f"Database Connection Failed: {e}")
    raw_df = pd.DataFrame()

# 5. TOP CENTER NAVIGATION
st.markdown('<h1 class="center-title">ECHOES 💎</h1>', unsafe_allow_html=True)
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([2, 1, 1, 1, 2])

if 'menu' not in st.session_state:
    st.session_state.menu = "explorer"

with nav_col3:
    if st.button("🔍 Job Explorer", use_container_width=True):
        st.session_state.menu = "explorer"
with nav_col4:
    if st.button("📊 Market Intelligence", use_container_width=True):
        st.session_state.menu = "analytics"

st.write("---")

# 6. SIDEBAR (Region Filter & Currency)
with st.sidebar:
    st.write("### Filters")
    if not raw_df.empty:
        # User requested 'Region' label instead of 'Active Regions'
        available_countries = sorted(raw_df['country'].unique().tolist())
        selected_countries = st.multiselect("Region", available_countries, default=available_countries[:3])
        
        currency = st.radio("Currency", ["USD", "INR"], horizontal=True)
        rate = 83.5 if currency == "INR" else 1.0
        
        filtered_df = raw_df[raw_df['country'].isin(selected_countries)]
    else:
        filtered_df = pd.DataFrame()

# 7. APP VIEWS
if not raw_df.empty:
    
    # ─── VIEW 1: JOB EXPLORER ───
    if st.session_state.menu == "explorer":
        st.write("### Find Your Next Role")
        # Ask for preference first
        role_pref = st.selectbox("What is your primary tech stack or target role?", ["Select a role..."] + TECH_ROLES)
        
        if role_pref != "Select a role...":
            explorer_df = filtered_df[filtered_df['title'].str.contains(role_pref, case=False)]
            
            if not explorer_df.empty:
                # Show Top 3 Recommendations
                st.write("#### ✨ Top 3 Recommendations for You")
                top_3 = explorer_df.sort_values(by='salary_max', ascending=False).head(3)
                
                for _, row in top_3.iterrows():
                    found_skills = [s for s in SKILL_KEYWORDS if s.lower() in (row['description'] or "").lower()]
                    skill_html = "".join([f'<span class="skill-badge">{s}</span>' for s in found_skills[:5]])
                    sal = f"{row['salary_min']*rate:,.0f} - {row['salary_max']*rate:,.0f} {currency}" if row['salary_min'] > 0 else "Competitive"
                    st.markdown(f"""
                        <div class="job-card top-match-card">
                            <a href="{row['url']}" target="_blank" style="float:right; background:#6366f1; color:white; padding:10px 20px; border-radius:12px; font-weight:700; text-decoration:none;">Apply</a>
                            <h2 style="margin-top:0;">{row['title']} <small style="font-size:12px; color:#818cf8;">BEST MATCH</small></h2>
                            <p style="color: #818cf8;">{row['company']} • 📍 {row['location']} ({row['country']})</p>
                            <div style="margin-top:10px; margin-bottom:15px;">{skill_html}</div>
                            <p style="color: #9ca3af; font-size: 0.9rem;">💰 <b>Est. Salary:</b> {sal}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.write("---")
                st.write(f"#### All {role_pref} Opportunities")
                remaining_df = explorer_df.iloc[3:] if len(explorer_df) > 3 else pd.DataFrame()
                
                if remaining_df.empty and len(explorer_df) <= 3:
                    st.info("Showing all available matches above.")
                else:
                    for _, row in remaining_df.iterrows():
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
                st.warning("No matches found for this specific role in the selected regions.")
        else:
            st.info("Please select your target role from the dropdown above to view job listings.")

    # ─── VIEW 2: MARKET ANALYTICS ───
    elif st.session_state.menu == "analytics":
        st.write("### Market Intelligence Reports")
        
        # 1. Salary Distribution
        st.write("#### 💸 Salary Benchmarking by Region")
        sal_clean = filtered_df[filtered_df['salary_min'] > 0]
        fig1 = px.box(sal_clean, x="country", y="salary_min", color="country", template="plotly_dark",
                      labels={"salary_min": f"Salary ({currency})", "country": "Region"})
        # Hover cleanup: only show Full Country Name
        fig1.update_traces(hovertemplate="<b>%{x}</b><br>Salary: %{y}<extra></extra>")
        fig1.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('<p class="desc-text">This diagram illustrates the salary variance across your selected regions. The central box represents the middle 50% of the market, while the dots indicate specific high-value outliers in the tech sector.</p>', unsafe_allow_html=True)

        # 2. Regional Demand
        st.write("#### 📊 Global Demand Distribution")
        fig2 = px.pie(filtered_df, names="country", hole=0.6, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Purples)
        fig2.update_traces(hovertemplate="<b>%{label}</b><br>Share: %{percent}<extra></extra>")
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<p class="desc-text">This chart breaks down the total volume of job postings by region. It helps identify which geographical markets are currently most active for tech recruitment, allowing you to focus your search on high-demand hubs.</p>', unsafe_allow_html=True)

        # 3. Skills Radar
        st.write("#### 🎯 Technical Skill Requirements")
        all_desc = " ".join(filtered_df['description'].fillna("").tolist()).lower()
        skill_counts = {s: all_desc.count(s.lower()) for s in SKILL_KEYWORDS}
        skill_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Mentions']).sort_values('Mentions', ascending=False)
        fig4 = px.line_polar(skill_df, r='Mentions', theta='Skill', line_close=True, template="plotly_dark")
        fig4.update_traces(fill='toself', line_color='#818cf8', hovertemplate="<b>%{theta}</b><br>Mentions: %{r}<extra></extra>")
        fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('<p class="desc-text">The radar chart tracks keyword frequency within job descriptions. A larger surface area indicates a higher cumulative demand for that specific technology across all active job postings in the selected regions.</p>', unsafe_allow_html=True)

else:
    st.warning("Database empty. Ensure your ETL pipeline is running.")
