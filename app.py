import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go

# 1. PAGE CONFIG
st.set_page_config(page_title="TechJobs Global Pro", page_icon="💎", layout="wide")

# 2. MAPPING & CONSTANTS
COUNTRY_MAP = {
    "at": "Austria", "au": "Australia", "be": "Belgium", "br": "Brazil", 
    "ca": "Canada", "ch": "Switzerland", "de": "Germany", "es": "Spain", 
    "fr": "France", "gb": "United Kingdom", "in": "India", "it": "Italy", 
    "mx": "Mexico", "nl": "Netherlands", "nz": "New Zealand", "pl": "Poland", 
    "sg": "Singapore", "us": "United States", "za": "South Africa"
}
SKILL_KEYWORDS = ["Python", "SQL", "AWS", "Azure", "Docker", "Kubernetes", "Spark", "React", "Tableau", "Snowflake", "Java"]

# 3. ELITE GLASSMORPHIC CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .main { background: radial-gradient(circle at top right, #1e1b4b, #020617); }
    
    /* KPI Card Styling */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 20px;
    }
    
    /* Navigation Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid #1e293b; }
    
    /* Job Card Styling */
    .job-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 24px;
        margin-bottom: 25px;
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
    df['country'] = df['country'].str.lower()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Database Connection Failed: {e}")
    df = pd.DataFrame()

# 5. NAVIGATION & SIDEBAR
with st.sidebar:
    st.title("ECHOES 💎")
    menu = st.radio("PLATFORM VIEW", ["🔍 Job Explorer", "📊 Market Intelligence"])
    st.divider()
    
    if not df.empty:
        # Global Filters
        available_codes = df['country'].unique().tolist()
        display_options = {COUNTRY_MAP.get(code, code.upper()): code for code in available_codes}
        selected_names = st.multiselect("Active Regions", list(display_options.keys()), default=list(display_options.keys())[:3])
        selected_codes = [display_options[name] for name in selected_names]
        
        currency = st.radio("Dashboard Currency", ["USD", "INR"], horizontal=True)
        rate = 83.5 if currency == "INR" else 1.0
        
        filtered_df = df[df['country'].isin(selected_codes)]

# 6. APP LOGIC BY PAGE
if not df.empty:
    
    # ─── VIEW 1: JOB EXPLORER ───
    if menu == "🔍 Job Explorer":
        st.title("Global Tech Explorer")
        st.write(f"Showing **{len(filtered_df)}** verified roles in your selected regions.")
        
        # Simple search filter inside Explorer
        search = st.text_input("Quick Search", placeholder="e.g. Data Engineer")
        if search:
            display_df = filtered_df[filtered_df['title'].str.contains(search, case=False)]
        else:
            display_df = filtered_df

        for _, row in display_df.iterrows():
            found_skills = [s for s in SKILL_KEYWORDS if s.lower() in (row['description'] or "").lower()]
            skill_html = "".join([f'<span class="skill-badge">{s}</span>' for s in found_skills[:5]])
            sal = f"{row['salary_min']*rate:,.0f} - {row['salary_max']*rate:,.0f} {currency}" if row['salary_min'] > 0 else "Competitive"

            st.markdown(f"""
                <div class="job-card">
                    <a href="{row['url']}" target="_blank" style="float:right; background:#6366f1; color:white; padding:10px 20px; border-radius:12px; font-weight:700; text-decoration:none;">Apply</a>
                    <h2>{row['title']}</h2>
                    <p style="color: #818cf8;">{row['company']} • 📍 {row['location']}</p>
                    <div style="margin-top:10px; margin-bottom:15px;">{skill_html}</div>
                    <p style="color: #9ca3af; font-size: 0.9rem;">💰 <b>Rate:</b> {sal}</p>
                </div>
            """, unsafe_allow_html=True)

    # ─── VIEW 2: MARKET ANALYTICS ───
    elif menu == "📊 Market Intelligence":
        st.title("Market Analytics Dashboard")
        st.write("Real-time salary benchmarking and regional demand analysis.")

        # KPI ROW
        c1, c2, c3 = st.columns(3)
        sal_clean = filtered_df[filtered_df['salary_min'] > 0]
        avg = (sal_clean['salary_min'].mean() + sal_clean['salary_max'].mean()) / 2 * rate if not sal_clean.empty else 0
        
        c1.metric("Market Sample Size", f"{len(filtered_df)} Jobs")
        c2.metric(f"Global Avg ({currency})", f"{avg:,.0f}" if avg > 0 else "N/A")
        c3.metric("Lead Hiring Region", filtered_df['country'].value_counts().idxmax().upper() if not filtered_df.empty else "N/A")

        st.divider()

        # ROW 1: SALARY & DEMAND
        row1_c1, row1_c2 = st.columns(2)
        with row1_c1:
            st.write("#### Salary Ranges by Country")
            fig1 = px.box(sal_clean, x="country", y="salary_min", color="country", template="plotly_dark")
            fig1.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)

        with row1_c2:
            st.write("#### Regional Demand (Share of Jobs)")
            fig2 = px.pie(filtered_df, names="country", hole=0.6, 
                         template="plotly_dark", 
                         color_discrete_sequence=px.colors.sequential.Purples)
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)
            
        # ROW 2: COMPANIES & SKILLS
        row2_c1, row2_c2 = st.columns(2)
        with row2_c1:
            st.write("#### Top 10 Hiring Companies")
            top_cos = filtered_df['company'].value_counts().nlargest(10).reset_index()
            top_cos.columns = ['company', 'count']
            fig3 = px.bar(top_cos, x="count", y="company", orientation='h', template="plotly_dark", color="count")
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig3, use_container_width=True)

        with row2_c2:
            st.write("#### Most Requested Technical Skills")
            all_desc = " ".join(filtered_df['description'].fillna("").tolist()).lower()
            skill_counts = {s: all_desc.count(s.lower()) for s in SKILL_KEYWORDS}
            skill_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Mentions']).sort_values('Mentions', ascending=False)
            
            fig4 = px.line_polar(skill_df, r='Mentions', theta='Skill', line_close=True, template="plotly_dark")
            fig4.update_traces(fill='toself', line_color='#818cf8')
            fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig4, use_container_width=True)

else:
    st.warning("Database is empty or connection failed. Please check your Supabase/Adzuna ETL pipeline.")
