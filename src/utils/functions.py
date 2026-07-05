from datetime import datetime
from wordfreq import zipf_frequency
from dotenv import load_dotenv
from os import getenv

def get_current_timestamp():
    return datetime.now().isoformat()


def get_s3_bucket():
    value = getenv('S3_BUCKET_NAME')
    if value:
        return getenv('S3_BUCKET_NAME')
    else:
        load_dotenv()
        return getenv('S3_BUCKET_NAME')


def get_env_variable(variable_name):
    value = getenv(variable_name)
    if value:
        return value
    else:
        load_dotenv()
        return getenv(variable_name)

def is_advanced_word(word):
    return (
        len(word) >= 4 and
        zipf_frequency(word, 'en') < 5.3
    )
