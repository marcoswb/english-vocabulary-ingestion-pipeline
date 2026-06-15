from datetime import datetime
from airflow.models import Variable
from wordfreq import zipf_frequency

def get_current_timestamp():
    return datetime.now().isoformat()


def get_s3_bucket():
    return Variable.get('S3_BUCKET_NAME')


def is_advanced_word(word):
    return (
        len(word) >= 4 and
        zipf_frequency(word, 'en') < 5.3
    )
