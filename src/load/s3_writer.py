import boto3
import json
from datetime import datetime
from src.utils.functions import get_s3_bucket
from src.load.s3_loader import load_metadata


s3 = boto3.client("s3")

def upload_json_to_s3(data, bucket, key):
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(data),
        ContentType="application/json",
    )

def save_vocab_data(data):
    bucket_name = get_s3_bucket()

    today = datetime.utcnow().strftime('%Y-%m-%d')
    key = f'raw/articles/date={today}/articles.json'

    upload_json_to_s3(data, bucket_name, key)
    return bucket_name, key


def save_metadata(data):
    bucket_name = get_s3_bucket()

    today = datetime.utcnow().strftime('%Y-%m-%d')
    key = f'raw/articles/date={today}/metadata.json'

    aux_data = load_metadata()
    if aux_data:
        data = {**aux_data, **data}

    upload_json_to_s3(data, bucket_name, key)
    return bucket_name, key
