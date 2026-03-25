import os
import boto3


def get_s3_client():
    return boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def download_file_from_s3(bucket_name: str, object_key: str, local_path: str):
    s3 = get_s3_client()
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    s3.download_file(bucket_name, object_key, local_path)
    return local_path