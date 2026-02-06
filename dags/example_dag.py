from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def hello_world():
    print('Hello Airflow! Pipeline funcionando 🎉')


with DAG(
    dag_id='example_hello_world',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@weekly',
    catchup=False,
    tags=['example', 'learning'],
) as dag:

    hello_task = PythonOperator(
        task_id='hello_world_task',
        python_callable=hello_world,
    )
