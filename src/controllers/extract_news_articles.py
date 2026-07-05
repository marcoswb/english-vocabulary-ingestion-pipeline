from datetime import datetime
import logging
from src.scrapers.bbc import BBC
from src.scrapers.cbc import CBC
from src.scrapers.the_guardian import TheGuardian
from src.load.s3_writer import save_vocab_data


class ExtractArticles:

    def run(self):
        logging.info('Starting extract_articles process')

        articles = self.fetch_articles()
        valid_articles = self.validate_articles(articles)
        s3_info = self.store_raw_articles_s3(valid_articles)
        self.register_extract_metadata(s3_info)

        logging.info('Extract articles process completed')

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def store_raw_articles_s3(store_articles):
        logging.info('store_raw_articles_s3')

        bucket_name, key = save_vocab_data(store_articles)
        return {
            'bucket': bucket_name,
            'key': key,
            'count': len(store_articles)
        }

    @staticmethod
    def register_extract_metadata(extract_info):
        logging.info('register_extract_metadata')

        metadata = {
            'execution_time': datetime.utcnow().isoformat(),
            'articles_saved': extract_info['count'],
            's3_path': f"s3://{extract_info['bucket']}/{extract_info['key']}"
        }

        logging.info(f'Extract metadata: {metadata}')
