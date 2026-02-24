from airflow.decorators import dag, task
from datetime import datetime
import logging


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
        sources = [
            {
                'source_id': 'bbc',
                'name': 'BBC News',
                'type': 'rss',
                'language': 'en',
                'category': 'general',
                'url': 'https://feeds.bbci.co.uk/news/rss.xml'
            },
            {
                'source_id': 'reuters',
                'name': 'Reuters',
                'type': 'rss',
                'language': 'en',
                'category': 'general',
                'url': 'https://ir.thomsonreuters.com/rss/news-releases.xml'
            },
            {
                'source_id': 'voa',
                'name': 'VOA Learning English',
                'type': 'rss',
                'language': 'en',
                'category': 'learning',
                'url': 'https://www.voanews.com/api/zb__qtl-vomx-tpeqrtqq'
            }
        ]

        logging.info(f'{len(sources)} sources defined')
        return sources

    @task
    def fetch_articles(sources):
        print(f'fetch_articles {sources}')
        return ''

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

    sources = define_sources()
    articles = fetch_articles(sources)
    data = validate_articles(articles)
    data = deduplicate_articles(data)
    data = store_raw_articles_s3(data)
    register_extract_metadata(data)


taskflow_dag()
