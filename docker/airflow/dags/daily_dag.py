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

#Function takes in a dataframe and return a transformed dataframe
def process_files(df):

    #delete any rows that dont have a name
    new_df = df[df.name.notnull()]

    #remove title from name
    title_front = ["Dr.","Mrs.","Ms.","Mr."]
    title_back = ["Jr."]
    new_df['name'] = new_df['name'].apply(lambda x : " ".join(str(x).split(" ")[1:]) if any(y in x for y in title_front) else x)
    new_df['name'] = new_df['name'].apply(lambda x : " ".join(str(x).split(" ")[:-1]) if any(y in x for y in title_back) else x)

    #remove any zeros prepended to the price field
    new_df['price'] = pd.to_numeric(new_df['price'])
    
    #split name 
    new_df[['first_name','last_name']] = new_df['name'].str.split(" ", n = 1, expand = True)
    
    #create a new field(columns) above_100 (boolean) when price is true
    new_df['above_100'] = (new_df['price'] > 100.00) 
    
    #rearrange columns
    new_df = new_df[['name', 'first_name', 'last_name', 'price', 'above_100']]
    
    return new_df


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