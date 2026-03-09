from airflow.decorators import dag, task
from datetime import datetime
import logging
from src.article_model import ArticleModel


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
        articles = []
        for source in sources:
            logging.info(f"Fetching articles from {source['name']} ({source['url']})")

            article = ArticleModel()
            article.source_id = source['source_id']

            articles.append(article)
            logging.info(f"Article fetched")

        return articles

    @task
    def validate_articles(data):
        logging.info('validate_articles')
        return []

    @task
    def deduplicate_articles(data):
        logging.info('deduplicate_articles')
        return []

    @task
    def store_raw_articles_s3(data):
        logging.info('store_raw_articles_s3')
        return []

    @task
    def register_extract_metadata(data):
        logging.info('register_extract_metadata')
        return []

    sources = define_sources()
    articles = fetch_articles(sources)
    data = validate_articles(articles)
    data = deduplicate_articles(data)
    data = store_raw_articles_s3(data)
    register_extract_metadata(data)


taskflow_dag()
