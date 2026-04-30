import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="Tech Job Market Dashboard", layout="wide")
st.title("Automated Tech Job Market & Salary Predictor")

@st.cache_data
def load_data():
    conn = psycopg2.connect(
        dbname=st.secrets["postgres"]["dbname"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        host=st.secrets["postgres"]["host"],
        port=st.secrets["postgres"]["port"]
    )
    query = "SELECT title, company, location, salary_min, salary_max FROM tech_jobs WHERE salary_min IS NOT NULL;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

if not df.empty:
    df['avg_salary'] = (df['salary_min'] + df['salary_max']) / 2

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Job Titles by Average Salary ($)")
        salary_by_title = df.groupby('title')['avg_salary'].mean().sort_values(ascending=False).head(10)
        st.bar_chart(salary_by_title)

    with col2:
        st.subheader("Job Openings by Location")
        jobs_by_location = df['location'].value_counts().head(10)
        st.bar_chart(jobs_by_location)

    st.subheader("Recent Job Listings")
    st.dataframe(df.sort_index(ascending=False).head(100))
else:
    st.warning("No data available in the database.")