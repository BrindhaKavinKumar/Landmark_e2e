import os
import time
from dotenv import load_dotenv
from prometheus_client import start_http_server

from app.processor import process_message
from app.sqs_consumer import receive_messages, delete_message, parse_message
from app.s3_helper import download_file_from_s3

load_dotenv()

TEMP_DIR = "tmp"
METRICS_PORT = 8000


if __name__ == "__main__":
    print("[INFO] AWS worker started. Polling SQS...")
    print(f"[INFO] Starting Prometheus metrics server on port {METRICS_PORT}")

    start_http_server(METRICS_PORT)
    os.makedirs(TEMP_DIR, exist_ok=True)

    while True:
        try:
            messages = receive_messages()

            if not messages:
                print("[INFO] No messages in SQS...")
                time.sleep(5)
                continue

            for raw_message in messages:
                receipt_handle = raw_message["ReceiptHandle"]
                body = parse_message(raw_message)

                print(f"[INFO] Received SQS message: {body}")

                if body["type"] == "TEST_EVENT":
                    print("[INFO] S3 test event received. Deleting and skipping.")
                    delete_message(receipt_handle)
                    continue

                store_id = body["store_id"]
                bucket = body["bucket"]
                object_key = body["object_key"]
                uploaded_at = body.get("uploaded_at")

                local_file_name = object_key.split("/")[-1]
                local_file_path = os.path.join(TEMP_DIR, local_file_name)

                download_file_from_s3(bucket, object_key, local_file_path)

                result = process_message({
                    "store_id": store_id,
                    "file_path": local_file_path,
                    "uploaded_at": uploaded_at,
                })

                print(f"[INFO] Processing result: {result}")

                if result["status"] in ["SUCCESS", "SKIPPED"]:
                    delete_message(receipt_handle)
                    print("[INFO] SQS message deleted after successful processing")
                elif result["status"] == "FAILED":
                    print("[WARN] Processing failed. Message not deleted, SQS will retry")

        except Exception as e:
            print(f"[ERROR] Worker loop failed: {e}")

        time.sleep(5)