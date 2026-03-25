from prometheus_client import Counter, Histogram

FILES_PROCESSED_TOTAL = Counter(
    "files_processed_total",
    "Total number of successfully processed files"
)

FILES_FAILED_TOTAL = Counter(
    "files_failed_total",
    "Total number of failed files"
)

FILES_SKIPPED_TOTAL = Counter(
    "files_skipped_total",
    "Total number of skipped files"
)

RECORDS_PROCESSED_TOTAL = Counter(
    "records_processed_total",
    "Total number of successfully processed records"
)

RECORDS_FAILED_TOTAL = Counter(
    "records_failed_total",
    "Total number of failed records"
)

PROCESSING_DURATION_SECONDS = Histogram(
    "processing_duration_seconds",
    "Time spent processing a file"
)