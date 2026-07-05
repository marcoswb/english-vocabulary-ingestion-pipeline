import boto3
import json
from src.utils.functions import get_s3_bucket


s3 = boto3.client("s3")

def load_last_raw():
    bucket_name = get_s3_bucket()

    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix="raw/articles/"
    )

    keys = [
        obj["Key"]
        for obj in response.get("Contents", [])
        if obj["Key"].endswith("articles.json")
    ]

    if not keys:
        raise ValueError("Nenhum arquivo encontrado no S3")

    latest_key = sorted(keys)[-1]

    response = s3.get_object(
        Bucket=bucket_name,
        Key=latest_key
    )

    file_content = response["Body"].read().decode("utf-8")

    return json.loads(file_content)


def load_metadata():
    bucket_name = get_s3_bucket()

    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix="raw/articles/"
    )

    keys = [
        obj["Key"]
        for obj in response.get("Contents", [])
        if obj["Key"].endswith("metadata.json")
    ]

    if not keys:
        return {}

    latest_key = sorted(keys)[-1]

    response = s3.get_object(
        Bucket=bucket_name,
        Key=latest_key
    )

    file_content = response["Body"].read().decode("utf-8")

    return json.loads(file_content)