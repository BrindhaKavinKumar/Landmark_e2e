import uuid
import time
from datetime import datetime

import pandas as pd
from sqlalchemy.exc import IntegrityError

from app.db import SessionLocal
from app.models import FileProcessing, RecordProcessing, ProductUpdate, ErrorLog
from app.validator import validate_record
from app.metrics import (
    FILES_PROCESSED_TOTAL,
    FILES_FAILED_TOTAL,
    FILES_SKIPPED_TOTAL,
    RECORDS_PROCESSED_TOTAL,
    RECORDS_FAILED_TOTAL,
    PROCESSING_DURATION_SECONDS,
)


def parse_datetime(dt_str: str):
    if not dt_str:
        return None
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


def process_message(message: dict):
    session = SessionLocal()
    file_id = uuid.uuid4()
    start_time = time.time()

    try:
        file_path = message["file_path"]
        file_name = file_path.split("/")[-1]
        store_id = str(message["store_id"])
        uploaded_at_str = message.get("uploaded_at")

        uploaded_at = parse_datetime(uploaded_at_str) or datetime.utcnow()

        # -----------------------------
        # Idempotency check
        # -----------------------------
        existing_file = session.query(FileProcessing).filter_by(
            store_id=store_id,
            file_name=file_name
        ).first()

        if existing_file and existing_file.status in ["SUCCESS", "PARTIAL_SUCCESS"]:
            print(f"[SKIP] File already processed: {file_name}")
            FILES_SKIPPED_TOTAL.inc()

            return {
                "status": "SKIPPED",
                "file_name": file_name,
                "reason": "already processed"
            }

        # -----------------------------
        # Create file tracking entry
        # -----------------------------
        file_entry = FileProcessing(
            file_id=file_id,
            store_id=store_id,
            file_name=file_name,
            source_path=file_path,
            status="PROCESSING",
            uploaded_at=uploaded_at,
            processing_started_at=datetime.utcnow(),
        )
        session.add(file_entry)
        session.commit()

        success_count = 0
        failed_count = 0

        # -----------------------------
        # Read file
        # -----------------------------
        df = pd.read_csv(file_path)
        total_records = len(df)

        for idx, row in df.iterrows():
            record = row.to_dict()
            errors = validate_record(record)

            if errors:
                failed_count += 1

                session.add(
                    RecordProcessing(
                        record_id=uuid.uuid4(),
                        file_id=file_id,
                        row_number=idx + 1,
                        sku=str(record.get("sku", "")),
                        status="FAILED",
                        error_message="; ".join(errors),
                    )
                )

                session.add(
                    ErrorLog(
                        error_id=uuid.uuid4(),
                        file_id=file_id,
                        row_number=idx + 1,
                        error_type="VALIDATION_ERROR",
                        error_message="; ".join(errors),
                        raw_data=record,
                    )
                )
            else:
                success_count += 1

                offer_price_value = record.get("offer_price")
                if pd.isna(offer_price_value):
                    offer_price_value = None
                else:
                    offer_price_value = float(offer_price_value)

                session.add(
                    RecordProcessing(
                        record_id=uuid.uuid4(),
                        file_id=file_id,
                        row_number=idx + 1,
                        sku=str(record.get("sku", "")),
                        status="SUCCESS",
                        error_message=None,
                    )
                )

                session.add(
                    ProductUpdate(
                        id=uuid.uuid4(),
                        file_id=file_id,
                        store_id=str(record["store_id"]),
                        sku=str(record["sku"]),
                        price=float(record["price"]),
                        offer_price=offer_price_value,
                        stock=int(record["stock"]),
                        campaign_id=str(record.get("campaign_id", "")),
                        last_updated=parse_datetime(str(record["last_updated"])),
                    )
                )

        # -----------------------------
        # Final file status update
        # -----------------------------
        file_entry.total_records = total_records
        file_entry.success_records = success_count
        file_entry.failed_records = failed_count
        file_entry.status = "SUCCESS" if failed_count == 0 else "PARTIAL_SUCCESS"
        file_entry.processing_completed_at = datetime.utcnow()

        session.commit()

        FILES_PROCESSED_TOTAL.inc()
        RECORDS_PROCESSED_TOTAL.inc(success_count)
        RECORDS_FAILED_TOTAL.inc(failed_count)

        print(f"[SUCCESS] File processed: {file_name}")
        print(
            f"[INFO] Total={total_records}, "
            f"Success={success_count}, Failed={failed_count}"
        )

        return {
            "status": "SUCCESS",
            "file_id": str(file_id),
            "file_name": file_name,
            "success_count": success_count,
            "failed_count": failed_count
        }

    except IntegrityError as e:
        session.rollback()
        FILES_SKIPPED_TOTAL.inc()

        print(f"[SKIP/DB-CONSTRAINT] Duplicate file detected: {e}")

        return {
            "status": "SKIPPED",
            "file_name": message.get("file_path", "").split("/")[-1],
            "reason": "duplicate file constraint hit"
        }

    except Exception as e:
        session.rollback()
        FILES_FAILED_TOTAL.inc()

        try:
            failed_file_name = message.get("file_path", "").split("/")[-1]
            failed_store_id = str(message.get("store_id", "unknown"))

            failed_file_entry = session.query(FileProcessing).filter_by(
                store_id=failed_store_id,
                file_name=failed_file_name
            ).first()

            if failed_file_entry:
                failed_file_entry.status = "FAILED"
                failed_file_entry.error_message = str(e)
                failed_file_entry.processing_completed_at = datetime.utcnow()
                session.commit()
        except Exception:
            session.rollback()

        print(f"[FAILED] File processing failed: {e}")

        return {
            "status": "FAILED",
            "file_name": message.get("file_path", "").split("/")[-1],
            "error": str(e)
        }

    finally:
        duration = time.time() - start_time
        PROCESSING_DURATION_SECONDS.observe(duration)
        session.close()