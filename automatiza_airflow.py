from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from save_raw_data_to_csv import save_csv
# from save_data_to_mongodb import save_mongo
from create_tables import create_tables
from transform_data import transform_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 13),
    'retries': 1
}

dag = DAG('automatic', default_args=default_args,
          schedule='@daily')


extract_to_file = PythonOperator(
    task_id='Save_to_file_raw_data',
    python_callable=save_csv,
    dag=dag
)

createtable = PythonOperator(
    task_id='Create_tables_postgres',
    python_callable=create_tables,
    dag=dag
)

save_cleaned_data_csv = PythonOperator(
    task_id='Save_to_CSV_Cleaned',
    python_callable=transform_data,
    dag=dag
)

save_on_dw = PythonOperator(
    task_id='Save_to_CSV_Cleaned',
    python_callable=create_tables,
    dag=dag
)

# mongodb= PythonOperator(
#     task_id='Save_raw_to_mongodb',
#     python_callable=save_mongo,
#     dag=dag
# )

# Pipeline of tasks
extract_to_file >> createtable >> save_cleaned_data_csv >> save_on_dw
