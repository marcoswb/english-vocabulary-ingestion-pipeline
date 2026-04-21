from airflow.decorators import dag, task
from datetime import datetime
import logging
from src.load.s3_loader import load_last_raw


@dag(
    dag_id='build_vocabulary_dataset',
    start_date=datetime(2024, 1, 1),
    schedule='@weekly',
    catchup=False,
    tags=['learning'],
)
def taskflow_dag():

    @task
    def load_raw_articles():
        logging.info('load_raw_articles')
        return load_last_raw()

    @task
    def build_corpus(input_articles):
        logging.info('build_corpus')
        print(input_articles)

        articles = []
        return articles

    @task
    def clean_text(input_articles):
        logging.info('clean_text')

        articles = []
        return articles

    @task
    def tokenize_words(input_articles):
        logging.info('tokenize_words')

        articles = []
        return articles

    @task
    def remove_stopwords(input_articles):
        logging.info('remove_stopwords')

        articles = []
        return articles

    @task
    def calculate_word_frequency(input_articles):
        logging.info('calculate_word_frequency')

        words = []
        return words

    @task
    def filter_candidate_words(input_words):
        logging.info('filter_candidate_words')

        words = []
        return words

    @task
    def filter_existing_words(input_words):
        logging.info('filter_existing_words')

        words = []
        return words

    @task
    def insert_new_words(input_words):
        logging.info('insert_new_words')

        return {}

    @task
    def register_dataset_metadata(insert_info):
        logging.info('register_dataset_metadata')

        return {}

    raw_articles = load_raw_articles()
    consolidated_articles = build_corpus(raw_articles)
    cleaned_articles = clean_text(consolidated_articles)
    tokenized_articles = tokenize_words(cleaned_articles)
    filtered_articles = remove_stopwords(tokenized_articles)
    list_word_frequency = calculate_word_frequency(filtered_articles)
    list_condidate_words = filter_candidate_words(list_word_frequency)
    list_filtered_words = filter_existing_words(list_condidate_words)
    s3_info = insert_new_words(list_filtered_words)
    register_dataset_metadata(s3_info)


taskflow_dag()
