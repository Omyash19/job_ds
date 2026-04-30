import streamlit as st
import pandas as pd
from sqlalchemy import create_client, create_engine
import os

# ═══════════════════════════════════════════════════════════════════════════
# 1. PAGE CONFIG & THEME
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(page_title="TechJobs Global", page_icon="🌐", layout="wide")

# Custom CSS for "SaaS" look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .job-card { background-color: white; padding: 20px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #eee; }
    .apply-btn { background-color: #6366f1; color: white !important; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# 2. DATA ENGINE (SUPABASE CONNECTION)
# ═══════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def load_data():
    # Using your existing DATABASE_URL secret
    db_url = st.secrets["DATABASE_URL"]
    engine = create_engine(db_url)
    query = "SELECT * FROM tech_jobs"
    df = pd.read_sql(query, engine)
    
    # Ensure country is lowercase for consistency
    if 'country' in df.columns:
        df['country'] = df['country'].str.lower()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not connect to Supabase: {e}")
    df = pd.DataFrame()

# ═══════════════════════════════════════════════════════════════════════════
# 3. SIDEBAR FILTERS
# ═══════════════════════════════════════════════════════════════════════════
st.sidebar.title("🌐 Global Controls")

if st.sidebar.button("🔄 Sync Latest Data"):
    st.cache_data.clear()
    st.rerun()

currency = st.sidebar.selectbox("Dashboard Currency", ["USD", "INR"])
exchange_rate = 83.5 if currency == "INR" else 1.0

# Dynamic Filters based on your LIVE data
if not df.empty:
    all_regions = sorted(df['country'].unique().tolist())
    selected_regions = st.sidebar.multiselect("Select Regions", all_regions, default=all_regions[:2])
    
    search_query = st.sidebar.text_input("Search Jobs or Companies")
    
    # Filtering Logic
    filtered_df = df[df['country'].isin(selected_regions)]
    if search_query:
        filtered_df = filtered_df[
            filtered_df['title'].str.contains(search_query, case=False) | 
            filtered_df['company'].str.contains(search_query, case=False)
        ]
else:
    filtered_df = pd.DataFrame()

# ═══════════════════════════════════════════════════════════════════════════
# 4. MAIN DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
st.title("🚀 Tech Job Market Intelligence")
st.write(f"Currently tracking **{len(filtered_df)}** active roles globally.")

# KPI Row
m1, m2, m3 = st.columns(3)
if not filtered_df.empty:
    avg_sal = (filtered_df['salary_min'].mean() + filtered_df['salary_max'].mean()) / 2 * exchange_rate
    top_co = filtered_df['company'].value_counts().idxmax()
    
    m1.metric("Total Jobs Found", len(filtered_df))
    m2.metric(f"Avg Salary ({currency})", f"{avg_sal:,.0f}")
    m3.metric("Top Hiring Company", top_co)

st.divider()

# Job Listing Loop (The "UI" part)
if not filtered_df.empty:
    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.subheader(f"{row['title']}")
                st.write(f"**{row['company']}** | 📍 {row['location']} ({row['country'].upper()})")
                st.caption(f"Salary Range: {row['salary_min'] * exchange_rate:,.0f} - {row['salary_max'] * exchange_rate:,.0f} {currency}")
            
            with col2:
                st.write("") # Spacing
                # This creates a real clickable button link
                st.markdown(f'<a href="{row["url"]}" target="_blank" class="apply-btn">Apply Here 🔗</a>', unsafe_allow_html=True)
            
            with st.expander("View Job Description"):
                st.write(row['description'])
            st.write("---")
else:
    st.info("Adjust the filters to see available job roles.")
