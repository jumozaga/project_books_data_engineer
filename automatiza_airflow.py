from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from save_data_to_csv import save_csv
from save_data_to_mongodb import save_mongo


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 13),
    'retries': 1
}

dag = DAG('automatic', default_args=default_args,
          schedule='@daily')


file_task = PythonOperator(
    task_id='Save_to_file',
    python_callable=save_csv,
    dag=dag
)

mongodb_task = PythonOperator(
    task_id='Save_to_mongodb',
    python_callable=save_mongo,
    dag=dag
)


file_task >> mongodb_task
