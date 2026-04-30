import os
import requests
import pandas as pd
from sqlalchemy import create_engine
import time

# 1. Pull secrets dynamically from GitHub Actions environment
APP_ID = os.environ.get('ADZUNA_APP_ID')
API_KEY = os.environ.get('ADZUNA_API_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')
SEARCH_TERM = 'Data Engineer'

# Supported Adzuna Countries
COUNTRIES = ['us', 'gb', 'in', 'ca', 'au', 'nz', 'at', 'be', 'br', 'ch', 'de', 'es', 'fr', 'it', 'mx', 'nl', 'pl', 'ru', 'za']

def extract_and_load_to_supabase():
    print("🚀 Starting global data extraction...")
    all_data = []
    
    # 2. Extract Data from Adzuna (Looping through countries and pages)
    for country in COUNTRIES:
        print(f"🌍 Fetching data for: {country.upper()}...")
        
        # Loop through Page 1 and Page 2 (50 jobs per page = up to 100 jobs per country)
        for page in range(1, 3): 
            url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}?app_id={APP_ID}&app_key={API_KEY}&results_per_page=50&what={SEARCH_TERM}"
            
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json().get('results', [])
                    for job in data:
                        job['country'] = country  # Mark the country for the database
                        job['url'] = job.get('redirect_url') # Grab the direct apply link!
                    
                    all_data.extend(data)
                else:
                    print(f"⚠️ API Error for {country.upper()} Page {page}! Status Code: {response.status_code}")
                
                time.sleep(1) # Be kind to the API to avoid rate limits
            except Exception as e:
                print(f"❌ Error fetching {country} Page {page}: {e}")

    print(f"✅ Found a total of {len(all_data)} jobs globally.")

    if not all_data:
        print("⚠️ No jobs found across any regions. Exiting.")
        return

    # 3. Transform the Data
    print("🔄 Cleaning data...")
    df = pd.DataFrame(all_data)
    
    # Extract strings from the nested dictionaries
    df['company'] = df['company'].apply(lambda x: x.get('display_name') if isinstance(x, dict) else x)
    df['location'] = df['location'].apply(lambda x: x.get('display_name') if isinstance(x, dict) else x)
    
    # Ensure all expected columns exist before saving (prevents errors if API returns empty fields)
    expected_columns = ['id', 'title', 'company', 'location', 'country', 'salary_min', 'salary_max', 'description', 'url']
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
            
    # Reorder to match database schema exactly
    df = df[expected_columns]
    
    # 4. Load Data to Supabase
    print("🔌 Connecting to Supabase...")
    try:
        engine = create_engine(DATABASE_URL)
        # Write to the database (if_exists='append' adds to the table without overwriting)
        df.to_sql('tech_jobs', engine, if_exists='append', index=False)
        print("🎉 SUCCESS! Global data inserted into Supabase!")
    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    extract_and_load_to_supabase()
