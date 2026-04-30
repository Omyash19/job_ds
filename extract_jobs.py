import requests
import pandas as pd
import boto3
from datetime import datetime
import io

# Configuration
APP_ID = 'YOUR_ADZUNA_APP_ID'
API_KEY = 'YOUR_ADZUNA_API_KEY'
S3_BUCKET = 'your-tech-jobs-bucket'
SEARCH_TERM = 'Data Engineer'

def extract_and_upload_to_s3():
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id={APP_ID}&app_key={API_KEY}&results_per_page=50&what={SEARCH_TERM}"
    response = requests.get(url)
    data = response.json().get('results', [])

    if not data:
        return

    # Transform
    df = pd.DataFrame(data)
    df = df[['id', 'title', 'company', 'location', 'salary_min', 'salary_max', 'description']]
    df['company'] = df['company'].apply(lambda x: x.get('display_name') if isinstance(x, dict) else x)
    df['location'] = df['location'].apply(lambda x: x.get('display_name') if isinstance(x, dict) else x)
    
    # Load to S3
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    filename = f"raw/jobs_{datetime.now().strftime('%Y%m%d')}.csv"
    
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=S3_BUCKET, Key=filename, Body=csv_buffer.getvalue())

if __name__ == "__main__":
    extract_and_upload_to_s3()