from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import json


def upload_json_to_s3(data, bucket, key):
    hook = S3Hook(aws_conn_id='aws_default')

    hook.load_string(
        string_data=json.dumps(data),
        key=key,
        bucket_name=bucket,
        replace=True
    )