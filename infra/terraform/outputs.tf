output "bucket_name" {
  value = aws_s3_bucket.retail_files.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.retail_files.arn
}

output "main_queue_url" {
  value = aws_sqs_queue.main.id
}

output "main_queue_arn" {
  value = aws_sqs_queue.main.arn
}

output "dlq_url" {
  value = aws_sqs_queue.dlq.id
}

output "dlq_arn" {
  value = aws_sqs_queue.dlq.arn
}