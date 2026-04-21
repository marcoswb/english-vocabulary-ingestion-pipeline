from airflow.decorators import dag, task
from datetime import datetime
from nltk.corpus import stopwords
import logging
import unicodedata
import re
from src.load.s3_loader import load_last_raw
from src.utils.functions import is_advanced_word, remove_entity_recognition


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

        articles = []
        for article in input_articles:
            articles.append(
                f"{article['title']} {article['full_text']}"
            )

        return articles

    @task
    def clean_text(input_articles_text):
        logging.info('clean_text')

        articles = []
        for article in input_articles_text:
            cleaned_article = article.lower()

            cleaned_article = unicodedata.normalize('NFD', cleaned_article)
            cleaned_article = cleaned_article.encode('ascii', 'ignore').decode('utf-8')

            cleaned_article = re.sub(r'[^a-zA-Z\s]', '', cleaned_article)
            cleaned_article = re.sub(r'\s+', ' ', cleaned_article)

            articles.append(cleaned_article.strip())

        return articles

    @task
    def tokenize_words(input_articles):
        logging.info('tokenize_words')

        words = []
        for article in input_articles:
            words.extend(remove_entity_recognition(article))

        return words

    @task
    def remove_stopwords(input_words):
        logging.info('remove_stopwords')

        words = []
        stop_words = set(stopwords.words('english'))
        for word in input_words:
            if word in stop_words:
                continue

            if len(word) <= 2:
                continue

            if not is_advanced_word(word):
                continue

            words.append(word)

        return words

    @task
    def calculate_word_frequency(input_words):
        logging.info('calculate_word_frequency')

        frequency = {}
        for word in input_words:
            frequency.setdefault(word, 0)
            frequency[word] += 1

        return frequency

    @task
    def filter_candidate_words(input_words):
        logging.info('filter_candidate_words')

        words = {}
        for word, freq in input_words.items():
            if freq >= 5:
                words[word] = freq

        return words

    @task
    def filter_existing_words(input_words):
        logging.info('filter_existing_words')

        words = {}
        for word, freq in input_words.items():
            if word not in ['example', 'test', 'sample']:
                words[word] = freq

        return words

    @task
    def insert_new_words(input_words):
        logging.info('insert_new_words')

        ordered_words = sorted(input_words.items(), key=lambda x: x[1], reverse=True)
        top_words = ordered_words[:5]
        print(top_words)

        return {
            'total_elegible_words': len(input_words),
            'inserted_words': len(top_words),
            'new_words': top_words
        }

    @task
    def register_dataset_metadata(insert_info):
        logging.info('register_dataset_metadata')

        metadata = {
            'execution_time': datetime.utcnow().isoformat(),
            'total_elegible_words': insert_info['total_elegible_words'],
            'inserted_words': insert_info['inserted_words'],
            'new_words': insert_info['new_words']
        }

        logging.info(f'Extract metadata: {metadata}')

    raw_articles = load_raw_articles()
    consolidated_articles = build_corpus(raw_articles)
    cleaned_articles = clean_text(consolidated_articles)
    tokenized_articles = tokenize_words(cleaned_articles)
    filtered_articles = remove_stopwords(tokenized_articles)
    dict_word_frequency = calculate_word_frequency(filtered_articles)
    dict_condidate_words = filter_candidate_words(dict_word_frequency)
    dict_filtered_words = filter_existing_words(dict_condidate_words)
    s3_info = insert_new_words(dict_filtered_words)
    register_dataset_metadata(s3_info)


taskflow_dag()
