#Import DAG object
from airflow import DAG 
#Import operators used in our tasks
from airflow.operators.python_operator import PythonOperator 
#Import days_ago function
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

# import necessary libraries
import pandas as pd
import os
import glob


# DAG directory path
dag_path = os.getcwd()


# Define arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["fxk_9370@hotmail.com"],  # Can change to the user of choice
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
    "start_date": datetime(2022, 7, 1),  # Change this date when first initialised
}

ingestion_dag = DAG(
    'booking_ingestion',
    default_args=default_args,
    description='Process and transform raw csv',
    schedule_interval=timedelta(days=1),
    catchup=False
)

task_1 = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=ingestion_dag,
)