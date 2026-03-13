from airflow.decorators import dag, task
from datetime import datetime
import logging
from src.scrapers.bbc import BBC
from src.scrapers.cbc import CBC
from src.scrapers.the_guardian import TheGuardian


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
        logging.info("Articles fetched")

        logging.info("Fetching articles from CBC")
        scraper = CBC()
        fetched_articles.extend(scraper.extract())
        logging.info("Articles fetched")

        logging.info("Fetching articles from The Guardian")
        scraper = TheGuardian()
        fetched_articles.extend(scraper.extract())
        logging.info("Articles fetched")

        return fetched_articles

    @task
    def validate_articles(data):
        logging.info('validate_articles')

        new_data = []
        for article in data:
            if not article.get('title') or not article.get('url'):
                continue

            if not article.get('full_text'):
                continue

            new_data.append(article)

        return new_data

    @task
    def store_raw_articles_s3(data):
        logging.info('store_raw_articles_s3')
        logging.info(f'Artigos para salvar: {len(data)}')
        return data

    @task
    def register_extract_metadata(data):
        logging.info('register_extract_metadata')

    articles = fetch_articles()
    filtered_articles = validate_articles(articles)
    stored_articles = store_raw_articles_s3(filtered_articles)
    register_extract_metadata(stored_articles)


taskflow_dag()
