from airflow.decorators import dag, task
from datetime import datetime
import logging
from src.scrapers.bbc import BBC


@dag(
    dag_id='extract_news_articles',
    start_date=datetime(2024, 1, 1),
    schedule='@weekly',
    catchup=False,
    tags=['learning'],
)
def taskflow_dag():

    @task
    def fetch_articles():
        fetched_articles = []

        logging.info("Fetching articles from BBC")
        scraper = BBC()
        fetched_articles.extend(scraper.extract())
        logging.info("Article fetched")

        return fetched_articles

    @task
    def validate_articles(data):
        logging.info('validate_articles')
        return data

    @task
    def deduplicate_articles(data):
        logging.info('deduplicate_articles')
        return data

    @task
    def store_raw_articles_s3(data):
        logging.info('store_raw_articles_s3')
        return data

    @task
    def register_extract_metadata(data):
        logging.info('register_extract_metadata')
        return data

    articles = fetch_articles()
    data = validate_articles(articles)
    data = deduplicate_articles(data)
    data = store_raw_articles_s3(data)
    register_extract_metadata(data)


taskflow_dag()
