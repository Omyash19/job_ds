from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
import io

default_args = {
    'owner': 'data_engineer',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_s3_to_rds(ds, **kwargs):
    s3_hook = S3Hook(aws_conn_id='aws_default')
    pg_hook = PostgresHook(postgres_conn_id='rds_postgres_conn')

    bucket_name = 'your-tech-jobs-bucket'
    file_key = f"raw/jobs_{ds.replace('-', '')}.csv"

    # Extract from S3
    file_obj = s3_hook.get_key(key=file_key, bucket_name=bucket_name)
    df = pd.read_csv(io.BytesIO(file_obj.get()['Body'].read()))

    # Load to RDS
    engine = pg_hook.get_sqlalchemy_engine()
    df.to_sql('tech_jobs', engine, if_exists='append', index=False)

with DAG(
    'tech_jobs_s3_to_rds',
    default_args=default_args,
    description='ETL pipeline moving daily job posts from S3 to RDS',
    schedule_interval='@daily',
    start_date=datetime(2023, 10, 1),
    catchup=False,
) as dag:

    load_data_task = PythonOperator(
        task_id='load_s3_data_to_rds',
        python_callable=load_s3_to_rds,
    )