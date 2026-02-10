from airflow.decorators import dag, task
from datetime import datetime


@dag(
    dag_id='extract_news_articles',
    start_date=datetime(2024, 1, 1),
    schedule='@weekly',
    catchup=False,
    tags=['learning'],
)
def taskflow_dag():

    @task
    def define_sources():
        print('define_sources')
        return 'dados extraídos'

    @task
    def fetch_articles(data):
        print('fetch_articles')
        return data.upper()

    @task
    def validate_articles(data):
        print('validate_articles')
        return data.upper()

    @task
    def deduplicate_articles(data):
        print('deduplicate_articles')
        return data.upper()

    @task
    def store_raw_articles_s3(data):
        print('store_raw_articles_s3')
        return data.upper()

    @task
    def register_extract_metadata(data):
        print('register_extract_metadata')
        return data.upper()

    data = define_sources()
    data = fetch_articles(data)
    data = validate_articles(data)
    data = deduplicate_articles(data)
    data = store_raw_articles_s3(data)
    register_extract_metadata(data)


taskflow_dag()
