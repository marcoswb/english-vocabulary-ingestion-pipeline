from airflow.decorators import dag, task
from datetime import datetime
from nltk.corpus import stopwords
import logging
import unicodedata
import re
import spacy
from wordfreq import zipf_frequency
from src.load.s3_loader import load_last_raw
from src.utils.functions import is_advanced_word
from src.models.vocabulary import Vocabulary
from src.models.candidate_words import CandidateWords

nlp = spacy.load('en_core_web_sm')

ENTITY_TYPES_TO_REMOVE = {
    'PERSON',
    'ORG',
    'GPE',
    'LOC',
    'NORP'
}


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
    def remove_named_entities(input_articles_text):
        logging.info('remove_named_entities')

        articles = []
        for doc in nlp.pipe(input_articles_text):

            tokens = []
            for token in doc:
                is_entity = (token.ent_type_ in ENTITY_TYPES_TO_REMOVE)

                if not is_entity:
                    tokens.append(token.text)

            articles.append(' '.join(tokens))

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
    def tokenize_lemmatize_words(input_articles):
        logging.info('tokenize_lemmatize_words')

        words = []
        for doc in nlp.pipe(input_articles):
            for token in doc:
                lemma = token.lemma_

                if lemma.isalpha():
                    words.append(lemma)

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

        vocab = Vocabulary()
        vocab.connect()

        existing_words = vocab.get_all_english_words()
        logging.info(f'Existing words in vocabulary: {len(existing_words)}')

        words = {}
        for word, freq in input_words.items():
            if word not in existing_words:
                try:
                    zipf_res = zipf_frequency(word, 'en')
                    words[word] = {
                        'frequency': freq,
                        'zipf_frequency': zipf_res,
                        'score': (
                            int(freq) * 0.6
                            + (5.3 - zipf_res) * 0.4
                        )
                    }
                except:
                    logging.warning(f'Error calculating zipf score for word: {word}')
                    continue

        return words

    @task
    def insert_new_words(input_words):
        logging.info('insert_new_words')

        top_words = []
        for word, infos in input_words.items():
            score = infos['score']

            if len(top_words) < 10:
                top_words.append((word, score))
            else:
                min_score = min(top_words, key=lambda x: x[1])[1]
                if score > min_score:
                    top_words = [w for w in top_words if w[1] != min_score]
                    top_words.append((word, score))

        for word, score in top_words:
            infos_aux = input_words[word]

            cand_word = CandidateWords()
            cand_word.connect()
            cand_word.insert_line(
                word=word,
                frequency=infos_aux['frequency'],
                zipf_score=infos_aux['zipf_frequency'],
                score=score
            )
            logging.info(f'Candidate word: {word} with score: {score}')

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
    filtered_articles_entities = remove_named_entities(consolidated_articles)
    cleaned_articles = clean_text(filtered_articles_entities)
    tokenized_words = tokenize_lemmatize_words(cleaned_articles)
    filtered_words = remove_stopwords(tokenized_words)
    dict_word_frequency = calculate_word_frequency(filtered_words)
    dict_condidate_words = filter_candidate_words(dict_word_frequency)
    dict_filtered_words = filter_existing_words(dict_condidate_words)
    s3_info = insert_new_words(dict_filtered_words)
    register_dataset_metadata(s3_info)


taskflow_dag()
