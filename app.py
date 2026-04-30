import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

# 1. PAGE CONFIG
st.set_page_config(page_title="TechJobs Global", page_icon="🚀", layout="wide")

# 2. COUNTRY MAPPING (Fixes Issue #1)
COUNTRY_MAP = {
    "at": "Austria", "au": "Australia", "be": "Belgium", "br": "Brazil", 
    "ca": "Canada", "ch": "Switzerland", "de": "Germany", "es": "Spain", 
    "fr": "France", "gb": "United Kingdom", "in": "India", "it": "Italy", 
    "mx": "Mexico", "nl": "Netherlands", "nz": "New Zealand", "pl": "Poland", 
    "ru": "Russia", "sg": "Singapore", "us": "United States", "za": "South Africa"
}

# 3. IMPROVED UI STYLING (Fixes unreadable Metrics)
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { color: #6366f1 !important; font-size: 32px; font-weight: 800; }
    [data-testid="stMetricLabel"] { color: #9ca3af !important; font-weight: 600; }
    .stMetric { background-color: #1e1b4b; padding: 20px; border-radius: 15px; border: 1px solid #312e81; }
    .job-card { background-color: #111827; padding: 25px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #1f2937; }
    .apply-btn { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white !important; padding: 10px 20px; border-radius: 10px; text-decoration: none; font-weight: bold; float: right; }
    </style>
""", unsafe_allow_html=True)

# 4. DATA ENGINE
@st.cache_data(ttl=3600)
def load_data():
    db_url = st.secrets["DATABASE_URL"]
    engine = create_engine(db_url)
    df = pd.read_sql("SELECT * FROM tech_jobs", engine)
    
    # Fix Salary Issues (Fixes "nan - nan")
    df['salary_min'] = pd.to_numeric(df['salary_min'], errors='coerce').fillna(0)
    df['salary_max'] = pd.to_numeric(df['salary_max'], errors='coerce').fillna(0)
    df['country'] = df['country'].str.lower()
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Connection failed. Check your DATABASE_URL.")
    df = pd.DataFrame()

# 5. SIDEBAR
st.sidebar.title("🌐 Global Controls")

if not df.empty:
    # Use full names in the dropdown (Fixes Issue #1)
    available_codes = df['country'].unique().tolist()
    display_options = {COUNTRY_MAP.get(code, code.upper()): code for code in available_codes}
    
    selected_names = st.sidebar.multiselect("Select Regions", list(display_options.keys()), default=list(display_options.keys())[:3])
    selected_codes = [display_options[name] for name in selected_names]

    # Improved Search (Prevents browser 'om' autofill)
    search_query = st.sidebar.text_input("Find a Role", placeholder="e.g. Engineer", autocomplete="off")

    currency = st.sidebar.selectbox("Currency", ["USD", "INR"])
    rate = 83.5 if currency == "INR" else 1.0

    filtered_df = df[df['country'].isin(selected_codes)]
    if search_query:
        filtered_df = filtered_df[filtered_df['title'].str.contains(search_query, case=False) | filtered_df['company'].str.contains(search_query, case=False)]
else:
    filtered_df = pd.DataFrame()

# 6. DASHBOARD
st.title("🚀 Tech Job Market Intelligence")

if not filtered_df.empty:
    col1, col2, col3 = st.columns(3)
    avg_sal = (filtered_df['salary_min'].mean() + filtered_df['salary_max'].mean()) / 2 * rate
    
    col1.metric("Total Jobs", len(filtered_df))
    col2.metric(f"Avg Salary ({currency})", f"{avg_sal:,.0f}")
    col3.metric("Top Hiring Company", filtered_df['company'].value_counts().idxmax())

    st.divider()

    for _, row in filtered_df.iterrows():
        st.markdown(f"""
            <div class="job-card">
                <a href="{row['url']}" target="_blank" class="apply-btn">Apply Here 🔗</a>
                <h3 style="margin-bottom: 5px;">{row['title']}</h3>
                <p style="color: #6366f1; font-weight: bold;">{row['company']} | 📍 {row['location']} ({row['country'].upper()})</p>
                <p style="font-size: 14px; color: #9ca3af;">Salary: {row['salary_min']*rate:,.0f} - {row['salary_max']*rate:,.0f} {currency}</p>
            </div>
        """, unsafe_allow_html=True)
        with st.expander("Role Details"):
            st.write(row['description'])
else:
    st.warning("No data found for current filters.")
