import json
import os
import boto3


def get_sqs_client():
    return boto3.client(
        "sqs",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def receive_messages():
    queue_url = os.getenv("SQS_QUEUE_URL")
    sqs = get_sqs_client()

    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10,
        VisibilityTimeout=30,
    )

    return response.get("Messages", [])


def delete_message(receipt_handle: str):
    queue_url = os.getenv("SQS_QUEUE_URL")
    sqs = get_sqs_client()

    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle,
    )


def parse_message(raw_message: dict):
    body = raw_message.get("Body", "{}")
    payload = json.loads(body)

    # Case 1: S3 test event
    if payload.get("Event") == "s3:TestEvent":
        return {
            "type": "TEST_EVENT",
            "bucket": payload.get("Bucket")
        }

    # Case 2: direct custom message
    if "store_id" in payload and "bucket" in payload and "object_key" in payload:
        return {
            "type": "CUSTOM_EVENT",
            "store_id": payload["store_id"],
            "bucket": payload["bucket"],
            "object_key": payload["object_key"],
            "uploaded_at": payload.get("uploaded_at")
        }

    # Case 3: real S3 object-created event
    if "Records" in payload and len(payload["Records"]) > 0:
        record = payload["Records"][0]
        object_key = record["s3"]["object"]["key"]
        bucket = record["s3"]["bucket"]["name"]

        # temp store_id extraction from filename
        file_name = object_key.split("/")[-1]
        store_id = "1001"
        if "store_" in file_name:
            try:
                store_id = file_name.split("_")[1]
            except Exception:
                store_id = "1001"

        return {
            "type": "S3_EVENT",
            "store_id": store_id,
            "bucket": bucket,
            "object_key": object_key,
            "uploaded_at": record.get("eventTime")
        }

    raise ValueError(f"Unsupported message format: {payload}")