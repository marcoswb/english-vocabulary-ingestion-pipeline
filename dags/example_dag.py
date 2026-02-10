from airflow.decorators import dag, task
from datetime import datetime


@dag(
    dag_id='taskflow_example',
    start_date=datetime(2024, 1, 1),
    schedule='@weekly',
    catchup=False,
    tags=['learning'],
)
def taskflow_dag():

    @task
    def extract():
        return 'dados extraídos'

    @task
    def transform(data):
        return data.upper()

    @task
    def load(data):
        print(f'Load: {data}')

    data = extract()
    transformed = transform(data)
    load(transformed)


taskflow_dag()
