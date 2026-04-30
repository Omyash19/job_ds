import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# 1. Page Configuration
st.set_page_config(
    page_title="Tech Job Market Intelligence",
    page_icon="💼",
    layout="wide"
)

# 2. Data Loading with Cache
@st.cache_data(ttl=3600)
def load_data():
    # Using the pooler URL from your secrets
    engine = create_engine(st.secrets["DATABASE_URL"])
    # Removed the WHERE filter so all jobs are visible
    return pd.read_sql("SELECT * FROM tech_jobs", engine)

df = load_data()

# 3. Sidebar Filtering Logic
st.sidebar.header("🔍 Filter Search")
if not df.empty:
    # Filter by Job Title
    all_titles = df['title'].unique().tolist()
    selected_titles = st.sidebar.multiselect("Select Job Titles:", all_titles, default=all_titles[:5])
    
    # Filter by Location
    all_locations = df['location'].unique().tolist()
    selected_locations = st.sidebar.multiselect("Select Locations:", all_locations, default=all_locations)

    # Apply filters
    filtered_df = df[
        (df['title'].isin(selected_titles)) & 
        (df['location'].isin(selected_locations))
    ]
else:
    filtered_df = df

# 4. Main UI Layout
st.title("🚀 Tech Job Market Insights")
st.markdown("Real-time data extracted via GitHub Actions and stored in Supabase.")

if not filtered_df.empty:
    # Calculate average salary for analytics
    filtered_df['avg_salary'] = (filtered_df['salary_min'] + filtered_df['salary_max']) / 2
    
    # --- KPI Metrics Row ---
    col1, col2, col3 = st.columns(3)
    avg_salary = filtered_df['avg_salary'].mean()
    
    with col1:
        st.metric("Total Jobs Found", len(filtered_df))
    with col2:
        st.metric("Avg Market Salary", f"${avg_salary:,.0f}" if not pd.isna(avg_salary) else "N/A")
    with col3:
        st.metric("Top Hiring Company", filtered_df['company'].mode()[0] if not filtered_df['company'].empty else "N/A")

    st.divider()

    # --- Navigation Tabs ---
    tab1, tab2 = st.tabs(["📊 Market Analytics", "🔍 Job Explorer"])

    with tab1:
        st.subheader("Salary Trends by Role")
        chart_data = filtered_df.groupby('title')['avg_salary'].mean().sort_values(ascending=False).head(10)
        if not chart_data.empty:
            st.bar_chart(chart_data)
        else:
            st.info("Not enough salary data to display trends. Try different filters.")

    with tab2:
        st.subheader("Current Openings")
        # Displaying clean data (hiding internal IDs for the user)
        cols_to_show = ['title', 'company', 'location', 'salary_min', 'salary_max', 'description']
        st.dataframe(filtered_df[cols_to_show], use_container_width=True, height=500)

else:
    if df.empty:
        st.warning("No data found in the database. Please run the ETL pipeline.")
    else:
        st.info("No results match your current filters. Try adjusting the sidebar settings.")

# 5. Footer Information
st.sidebar.divider()
st.sidebar.info(f"Last sync: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
