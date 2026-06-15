from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import json
from src.utils.functions import get_s3_bucket


def load_last_raw():
    hook = S3Hook(aws_conn_id='aws_default')
    bucket_name = get_s3_bucket()

    keys = hook.list_keys(
        bucket_name=bucket_name,
        prefix='raw/articles/'
    )

    keys = [
        k for k in keys
        if k.endswith('articles.json')
    ]

    if not keys:
        raise ValueError('Nenhum arquivo encontrado no S3')

    latest_key = sorted(keys)[-1]
    file_content = hook.read_key(key=latest_key, bucket_name=bucket_name)

    return json.loads(file_content)


def load_metadata():
    hook = S3Hook(aws_conn_id='aws_default')
    bucket_name = get_s3_bucket()

    keys = hook.list_keys(
        bucket_name=bucket_name,
        prefix='raw/articles/'
    )

    keys = [
        k for k in keys
        if k.endswith('metadata.json')
    ]

    if not keys:
        raise ValueError('Nenhum arquivo encontrado no S3')

    latest_key = sorted(keys)[-1]
    file_content = hook.read_key(key=latest_key, bucket_name=bucket_name)

    return json.loads(file_content)