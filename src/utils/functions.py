from datetime import datetime
from airflow.models import Variable
from wordfreq import zipf_frequency
import spacy

nlp = spacy.load('en_core_web_sm')

def get_current_timestamp():
    return datetime.now().isoformat()


def get_s3_bucket():
    return Variable.get('S3_BUCKET_NAME')


def is_advanced_word(word):
    return (
        len(word) >= 4 and
        zipf_frequency(word, 'en') < 4.5
    )

def remove_entity_recognition(text):
    doc = nlp(text)
    return [
        token.text
        for token in doc
        if not token.ent_type_
    ]
