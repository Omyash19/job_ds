import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# 1. Page Configuration
st.set_page_config(
    page_title="Global Tech Job Intelligence",
    page_icon="🌍",
    layout="wide"
)

# --- GLOBAL SETTINGS ---
COUNTRY_MAP = {
    'us': {'name': 'United States', 'flag': '🇺🇸', 'currency': 'USD', 'symbol': '$', 'rate': 1.0},
    'in': {'name': 'India', 'flag': '🇮🇳', 'currency': 'INR', 'symbol': '₹', 'rate': 0.012}, # Approx rate to USD
    'gb': {'name': 'United Kingdom', 'flag': '🇬🇧', 'currency': 'GBP', 'symbol': '£', 'rate': 1.25},
    'ca': {'name': 'Canada', 'flag': '🇨🇦', 'currency': 'CAD', 'symbol': 'C$', 'rate': 0.73},
    'de': {'name': 'Germany', 'flag': '🇩🇪', 'currency': 'EUR', 'symbol': '€', 'rate': 1.08}
}

# 2. Data Loading with Cache
@st.cache_data(ttl=3600)
def load_data():
    engine = create_engine(st.secrets["DATABASE_URL"])
    # Ensure the country column is included in your SELECT
    return pd.read_sql("SELECT * FROM tech_jobs", engine)

df = load_data()

# 3. Sidebar - Global Controls
st.sidebar.header("🌍 Global Controls")

# Base Currency Selection (For the KPI Metrics)
base_currency = st.sidebar.selectbox("Dashboard Currency:", ["USD", "INR"], index=0)
fx_rate = 83.0 if base_currency == "INR" else 1.0
currency_symbol = "₹" if base_currency == "INR" else "$"

if not df.empty:
    # Region Filter with Flags
    all_countries = df['country'].unique().tolist() if 'country' in df.columns else ['us']
    selected_countries = st.sidebar.multiselect(
        "Select Regions:",
        options=all_countries,
        default=all_countries,
        format_func=lambda x: f"{COUNTRY_MAP.get(x, {}).get('flag', '🌐')} {COUNTRY_MAP.get(x, {}).get('name', x.upper())}"
    )

    # Job Title Filter
    all_titles = df['title'].unique().tolist()
    selected_titles = st.sidebar.multiselect("Filter Job Titles:", all_titles, default=all_titles[:5])

    # Apply Filtering
    filtered_df = df[
        (df['country'].isin(selected_countries) if 'country' in df.columns else True) & 
        (df['title'].isin(selected_titles))
    ].copy()
else:
    filtered_df = df

# 4. Main UI Layout
st.title("🌍 Global Tech Job Market Insights")
st.markdown(f"Currently tracking jobs across **{len(filtered_df['country'].unique()) if 'country' in filtered_df.columns else 1}** regions.")

if not filtered_df.empty:
    # --- DATA NORMALIZATION (Handling multiple currencies) ---
    def normalize_salary(row):
        c_code = row.get('country', 'us')
        # Get rate for that country relative to USD, then convert to selected Base Currency
        usd_val = ((row['salary_min'] + row['salary_max']) / 2) * COUNTRY_MAP.get(c_code, {}).get('rate', 1.0)
        return usd_val * fx_rate

    filtered_df['normalized_avg'] = filtered_df.apply(normalize_salary, axis=1)

    # --- KPI Metrics Row ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Jobs Found", len(filtered_df))
    with col2:
        avg_sal = filtered_df['normalized_avg'].mean()
        st.metric(f"Avg Salary ({base_currency})", f"{currency_symbol}{avg_sal:,.0f}" if not pd.isna(avg_sal) else "N/A")
    with col3:
        top_comp = filtered_df['company'].mode()[0] if not filtered_df['company'].empty else "N/A"
        st.metric("Top Hiring Company", top_comp)

    st.divider()

    # --- Navigation Tabs ---
    tab1, tab2 = st.tabs(["📊 Market Analytics", "🔍 Global Job Explorer"])

    with tab1:
        st.subheader("Salary Trends by Role (Normalized)")
        chart_data = filtered_df.groupby('title')['normalized_avg'].mean().sort_values(ascending=False).head(10)
        if not chart_data.empty:
            st.bar_chart(chart_data)
        else:
            st.info("Insufficient salary data for these filters.")

    with tab2:
        st.subheader("Detailed Listings")
        
        # Add a visual Flag column to the explorer table
        explorer_df = filtered_df.copy()
        if 'country' in explorer_df.columns:
            explorer_df['region'] = explorer_df['country'].apply(lambda x: f"{COUNTRY_MAP.get(x, {}).get('flag', '🌐')} {x.upper()}")
        
        cols_to_show = (['region'] if 'country' in explorer_df.columns else []) + \
                       ['title', 'company', 'location', 'salary_min', 'salary_max', 'description']
        
        st.dataframe(explorer_df[cols_to_show], use_container_width=True, height=500)

else:
    st.info("No data found for the selected filters. Try broadening your search!")

# 5. Footer Information
st.sidebar.divider()
st.sidebar.caption(f"Last data refresh: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
