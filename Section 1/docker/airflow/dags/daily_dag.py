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

def transform_data():
    #change the raw_path according to your own raw folder path
    # raw_path = 'C:\\Users\\User\\OneDrive\\Desktop\\dsaid-de-tech-assessment\\docker\\airflow\\raw_data'
    raw_path = r'C:\Users\User\OneDrive\Desktop\dsaid-de-tech-assessment\Section 1\docker\airflow\raw_data'

    #change the raw_path according to your own processed folder path    
    # processed_path = 'C:\\Users\\User\\OneDrive\\Desktop\\dsaid-de-tech-assessment\\docker\\airflow\\processed_data'
    processed_path = r'C:\Users\User\OneDrive\Desktop\dsaid-de-tech-assessment\Section 1\docker\airflow\processed_data'

    # use glob to get all the csv files in the raw folder
    csv_files = glob.glob(os.path.join(raw_path, "*.csv"))
    
    # loop over the list of csv files
    for f in csv_files:

        # read the csv file
        df = pd.read_csv(f)
        # process and transform file
        df = process_files(df)

        #rename the file name by adding processed infront
        file_name = "processed_"+ f.split("\\")[-1]

        # save processed dataset in processed folder
        df.to_csv(f"{processed_path}/{file_name}", index=False)

        #remove raw dataset file once processed
        os.remove(f)


# Define arguments for the DAG
default_args = {
    "owner": "airflow",
    # "depends_on_past": False,
    # "email": ["fxk_9370@hotmail.com"],  # Can change to the user of choice
    # "email_on_failure": True,
    # "email_on_retry": True,
    # "retries": 2,
    # "retry_delay": timedelta(minutes=10),
    "start_date": days_ago(2),  # Change this date when first initialised
}

ingestion_dag = DAG(
    'ingestion_transform_dataset',
    default_args=default_args,
    description='Process and transform raw csv',
    # schedule_interval=timedelta(days=1),
    schedule_interval='0 1 * * *',    #to start DAG daily on 1am 
    catchup=False
)

task_1 = PythonOperator(
    task_id='transform_data',
    python_callable= transform_data,
    dag=ingestion_dag,
)

task_1
