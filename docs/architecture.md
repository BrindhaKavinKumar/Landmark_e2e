## Flow

1. CSV file is uploaded to S3 (simulated locally in `sample-files/`)
2. Worker service picks up the file
3. File entry is created in file_processing table (status = PENDING)

4. File-level validation:
   - correct format
   - required columns present

5. Record-level validation:
   - store_id required
   - sku required
   - price > 0
   - offer_price <= price
   - stock >= 0

6. Valid records are processed and stored in database
7. Invalid records are logged; persistent failures sent to DLQ
8. File and record statuses are updated (SUCCESS / FAILED)
9. API service exposes processed data
10. Infrastructure managed via Terraform and Kubernetes