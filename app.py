import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Tech Job Market", layout="wide")
@st.cache_data(ttl=3600) # This tells Streamlit to refresh the data every 1 hour (3600 seconds)
def load_data():
    engine = create_engine(st.secrets["DATABASE_URL"])
    return pd.read_sql("SELECT * FROM tech_jobs WHERE salary_min IS NOT NULL", engine)

df = load_data()

if not df.empty:
    df['avg_salary'] = (df['salary_min'] + df['salary_max']) / 2
    st.bar_chart(df.groupby('title')['avg_salary'].mean().head(10))
    st.dataframe(df.head(100))
else:
    st.warning("No data available in the database yet.")
