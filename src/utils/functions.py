from datetime import datetime
from airflow.models import Variable


def get_current_timestamp():
    return datetime.now().isoformat()


def get_s3_bucket():
    return Variable.get('S3_BUCKET_NAME')
