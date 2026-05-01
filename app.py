Ah, it looks like you accidentally copied some of the chat's metadata text (`Viewed app.py:1-328`) along with the code!

Please make sure you only copy the code starting from **`import streamlit as st`**.

Here is the exact code again. If your chat interface has a **"Copy Code"** button in the top right corner of this block, use that—it will safely copy only the Python code:

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import random

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
                sel_role = st.selectbox("Specify Tech Stack Preference", ["All Roles"] + TECH_ROLES)
            
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
        role_display = f["role"] if f["role"] != "All Roles" else "Tech Roles"
        st.markdown(f'<h3 style="color:#0f172a;">🔍 Explorer: {role_display} in {", ".join(f["regions"])}</h3>', unsafe_allow_html=True)
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
        
        if not sal_clean.empty:
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
            st.info("Not enough salary data to generate chart.")

else:
    st.error("Engine failure. Please check your connection.")
```
