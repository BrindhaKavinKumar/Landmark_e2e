variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "retail-platform"
}

variable "bucket_name" {
  description = "S3 bucket name"
  type        = string
}

variable "main_queue_name" {
  description = "Main SQS queue name"
  type        = string
  default     = "retail-file-events-tf"
}

variable "dlq_name" {
  description = "Dead letter queue name"
  type        = string
  default     = "retail-file-events-dlq-tf"
}

variable "max_receive_count" {
  description = "How many times SQS retries before DLQ"
  type        = number
  default     = 3
}