import os
import requests
import pandas as pd
from sqlalchemy import create_engine

# 1. Pull secrets dynamically from GitHub Actions environment
APP_ID = os.environ.get('ADZUNA_APP_ID')
API_KEY = os.environ.get('ADZUNA_API_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')
SEARCH_TERM = 'Data Engineer'

def extract_and_load_to_supabase():
    print("🚀 Starting data extraction...")
    
    # 2. Extract Data from Adzuna
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id={APP_ID}&app_key={API_KEY}&results_per_page=50&what={SEARCH_TERM}"
    response = requests.get(url)
    
    # Check if Adzuna is angry with us
    if response.status_code != 200:
        print(f"❌ API Error! Status Code: {response.status_code}")
        print(response.text)
        return

    data = response.json().get('results', [])
    print(f"✅ Found {len(data)} jobs from Adzuna.")

    if not data:
        print("⚠️ No jobs found. Exiting.")
        return

    # 3. Transform the Data
    print("🔄 Cleaning data...")
    df = pd.DataFrame(data)
    
    # Select only the columns that match your Supabase table
    df = df[['id', 'title', 'company', 'location', 'salary_min', 'salary_max', 'description']]
    
    # Extract strings from the nested dictionaries
    df['company'] = df['company'].apply(lambda x: x.get('display_name') if isinstance(x, dict) else x)
    df['location'] = df['location'].apply(lambda x: x.get('display_name') if isinstance(x, dict) else x)
    
    # 4. Load Data to Supabase
    print("🔌 Connecting to Supabase...")
    try:
        engine = create_engine(DATABASE_URL)
        # Write to the database (if_exists='append' adds to the table without overwriting)
        df.to_sql('tech_jobs', engine, if_exists='append', index=False)
        print("🎉 SUCCESS! Data inserted into Supabase!")
    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    extract_and_load_to_supabase()
