resource "aws_s3_bucket" "retail_files" {
  bucket = var.bucket_name

  tags = {
    Name        = var.bucket_name
    Project     = var.project_name
    Environment = "dev"
  }
}

resource "aws_s3_bucket_versioning" "retail_files_versioning" {
  bucket = aws_s3_bucket.retail_files.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_sqs_queue" "dlq" {
  name = var.dlq_name

  tags = {
    Name        = var.dlq_name
    Project     = var.project_name
    Environment = "dev"
  }
}

resource "aws_sqs_queue" "main" {
  name = var.main_queue_name

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = var.max_receive_count
  })

  tags = {
    Name        = var.main_queue_name
    Project     = var.project_name
    Environment = "dev"
  }
}

resource "aws_sqs_queue_policy" "allow_s3_send" {
  queue_url = aws_sqs_queue.main.id

  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "AllowS3SendMessage"
    Statement = [
      {
        Sid    = "AllowS3BucketToSendMessage"
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
        Action   = "SQS:SendMessage"
        Resource = aws_sqs_queue.main.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_s3_bucket.retail_files.arn
          }
          StringEquals = {
            "aws:SourceAccount" = data.aws_caller_identity.current.account_id
          }
        }
      }
    ]
  })
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.retail_files.id

  queue {
    queue_arn     = aws_sqs_queue.main.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "incoming/"
  }

  depends_on = [aws_sqs_queue_policy.allow_s3_send]
}