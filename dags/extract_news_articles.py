from airflow.decorators import dag, task
from datetime import datetime
import logging
from src.scrapers.bbc import BBC
from src.scrapers.cbc import CBC
from src.scrapers.the_guardian import TheGuardian
from src.load.s3_writer import save_vocab_data


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
    def validate_articles(list_articles):
        logging.info('validate_articles')

        new_data = []
        for article in list_articles:
            if not article.get('title') or not article.get('url'):
                continue

            if not article.get('full_text'):
                continue

            new_data.append(article)

        return new_data

    @task
    def store_raw_articles_s3(store_articles):
        logging.info('store_raw_articles_s3')

        bucket_name, key = save_vocab_data(store_articles)
        return {
            'bucket': bucket_name,
            'key': key,
            'count': len(store_articles)
        }

    @task
    def register_extract_metadata(extract_info):
        logging.info('register_extract_metadata')

        metadata = {
            'execution_time': datetime.utcnow().isoformat(),
            'articles_saved': extract_info['count'],
            's3_path': f"s3://{extract_info['bucket']}/{extract_info['key']}"
        }

        logging.info(f'Extract metadata: {metadata}')

    articles = fetch_articles()
    valid_articles = validate_articles(articles)
    s3_info = store_raw_articles_s3(valid_articles)
    register_extract_metadata(s3_info)


taskflow_dag()
